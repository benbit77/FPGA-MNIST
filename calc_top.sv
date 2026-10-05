module calc_top
	(
	input logic [9:0] SW,
	input logic [1:0] KEY,
	output logic [9:0] LEDR,
	output logic [6:0] HEX5,
	output logic [6:0] HEX4,
	output logic [6:0] HEX3,
	output logic [6:0] HEX2,
	output logic [6:0] HEX1,
	output logic [6:0] HEX0
	);
	
		logic [3:0] val_A;
		logic [3:0] val_B;
		logic [4:0] sum;
		
		
		register reg_A (
			.clk(KEY[1]),
			.reset(KEY[0]),
			.en(SW[9]),
			.d(SW[3:0]),
			.q(val_A)
		);

		register reg_B (
			.clk(KEY[1]),
			.reset(KEY[0]),
			.en(SW[8]),
			.d(SW[3:0]),
			.q(val_B)
		);
		
		assign sum = val_A + val_B;
		
		sevenseg seg_A (
			.d(val_A[3:0]),
			.segments(HEX5[6:0])
			);
			
		sevenseg seg_B (
			.d(val_B[3:0]),
			.segments(HEX3[6:0])
			);
			
		assign HEX2[6:0] = 7'b1111111;
		assign HEX4[6:0] = 7'b1111111;
		
		sevenseg seg_Sum_Left (
			.d({3'b000, sum[4]}),
			.segments(HEX1[6:0])
		);
		
		sevenseg seg_Sum_Right (
			.d(sum[3:0]),
			.segments(HEX0[6:0])
		);
		
		assign LEDR[9:0] = SW[9:0];
	
	
endmodule