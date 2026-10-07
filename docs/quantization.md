Scheme Review:
- What: Quantized weights, biases, and activations of the trained MLP, for integer-only inference on the MAX10 FPGA (no floating-point units).
- Multiplier convention: q = round(x * s); dequantization divides by s.
- int8: weights, inputs, activations.
- int32: biases, accumulators.

Scale factors:
s_x = 127
From: Chosen
Purpose: Input multiplier: converts normalized pixels in [0, 1] to int8 in [0, 127].

s_w1 = 202.5147
From: s_w1 = s_x / W1.abs().max()
Purpose: Weight multiplier: maps the layer-1 float weights onto the signed int8 range [-127, 127]. The .abs().max() finds the largest weight magnitude so the full range is used; the quantized weights stay signed and can be negative.

s_w2 = 133.7849
From: s_w2 = s_x / W2.abs().max()
Purpose: Same job for the layer-2 weights.

s_act = 6.910044727478284
From: 127 / max_act
Purpose: Activation multiplier: max_act is the largest of the 64 hidden-layer values seen on training data; the scale maps activations into int8 [0, 127].

Integer inference: layer 1
- Inputs are q_x (int8, each = round(pixel * s_x)) and q_w1 (int8, each = round(weight * s_w1)).
- Each hidden unit accumulates acc1[i] = Σ q_x[j]·q_w1[i][j] + q_b1[i] into int32; the bias is pre-scaled so it adds directly with no runtime work.
- ReLU and requantization fuse into one step: q_a1[i] = round(max(0, acc1[i]) · s_act / (s_x · s_w1)), constant ≈ 0.0002687. max(0, ·) before scaling is valid because the denominator is positive.

Integer inference: layer 2
- Same pattern with different tensors: inputs are q_a1 (int8) with scales s_act and s_w2, accumulating acc2[k] = Σ q_a1[i]·q_w2[k][i] + q_b2[k] into int32.
- No requantization at the end (unlike layer 1).

Bias handling
- Biases are pre-scaled into int32 accumulator units: q_b = round(b · s_in · s_w), the input scale times that layer's weight scale.
- This puts the bias in the same units as the products, so it drops straight into the accumulator with no runtime scaling.

Output layer (argmax)
- Returns the index of the largest layer-2 accumulator value.
- No requantization: a common positive scale factor cannot change which value is largest.

Accuracy results
- Float inference, full network: 96.73%.
- Integer-only inference, full network: 96.69%.
- Drop: 0.04%, within the 1-2% target. Cost comes from the two rounding points: quantizing weights/inputs and the requantization step.

Hardware implications
- int8 x int8 products are int16 (max 16129).
- Layer 1 sums 784 of them (about 12.6M worst case); layer 2 sums 64 (about 1M). Both need int32 accumulators.
- The requantization multiply becomes fixed-point in hardware: multiply by 282 then shift right 20 (282/2^20 ≈ 0.00026894, within 0.1% of the true constant), with a 64-bit intermediate at the worst-case bound.
