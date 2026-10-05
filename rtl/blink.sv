module blink
	(
	input logic CLOCK_50,
	output logic [9:0] LEDR
	);
	
	logic [24:0] count = 0;
	assign LEDR[9:1] = 9'b00000000;
	
	always_ff @(posedge CLOCK_50)
		begin
			if(count == 24999999)
				begin
					LEDR[0] <= ~LEDR[0];
					count <= 0;
				end
			else	
			count <= count + 1;
		end
	
endmodule