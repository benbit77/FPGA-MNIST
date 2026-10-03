# FPGA MNIST Accelerator

MNIST digit classifier as digital logic: SystemVerilog neural-network
inference engine on a DE10-Lite FPGA, 8-bit fixed point, Python-trained
and quantized.

## Status

Phase 0: toolchain bring-up. Project is just getting started.

## What this is

A 784 -> 64 -> 10 multilayer perceptron that classifies handwritten digits,
with inference running entirely as digital logic on an Intel MAX 10 FPGA
(Terasic DE10-Lite). Python trains the network and quantizes it to 8-bit
fixed point; the FPGA holds the weights in on-chip memory and runs the
multiply-accumulate datapath, ReLU activations, and argmax in hardware.
Test images are stored on-chip and selected with the slide switches; the
predicted digit shows on the 7-seg displays and the expected label on the
LEDs. Zero external parts: everything is on the board.

## Hardware

- Terasic DE10-Lite (Intel MAX 10 FPGA)

## Repo structure

- `rtl/` — SystemVerilog sources (MAC unit, layer FSM, argmax, top level)
- `tb/` — SystemVerilog testbenches, checked against the Python golden model
- `py/` — training, quantization, and golden-model scripts
- `weights/` — exported HEX/MIF weight and test-image files
- `docs/` — notes, block diagram, quantization analysis

## Roadmap

- [ ] Phase 0: Quartus + SystemVerilog sanity check on the board
- [ ] Phase 1: Python model, 8-bit quantization, golden model
- [ ] Phase 2: MAC unit, testbench-verified
- [ ] Phase 3: layer engine, ReLU, argmax
- [ ] Phase 4: weight/image ROMs, top-level integration, full-system sim
- [ ] Phase 5: hardware bring-up, 16/16 test images correct
- [ ] Phase 6: demo video

## How to build

Requires Intel Quartus Prime. Open the project in Quartus, compile, and program
the DE10-Lite over USB-Blaster. (Details to come as the build takes shape.)

## Design approach

Golden-model first: a pure-Python fixed-point model of the network is the
reference that every RTL testbench checks against. Nothing goes on hardware
until simulation matches the golden model.

## License

MIT
