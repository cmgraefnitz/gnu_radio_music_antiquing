"""
Embedded Python Block: Add AWGN with SNR and Noise Floor
"""

import numpy as np
from gnuradio import gr

class blk(gr.sync_block):
    """Adds AWGN with configurable SNR and minimum noise floor"""
    
    def __init__(self, snr=10.0, noise_offset=-40.0):
        gr.sync_block.__init__(
            self,
            name='Add AWGN',
            in_sig=[np.float32],
            out_sig=[np.float32]
        )
        self.snr = snr
        self.noise_offset = noise_offset
        self.rng = np.random.default_rng()
        
        # Convert noise floor from dB to power (10^(dB/10))
        self.offset_power = 10**(self.noise_offset/10)

    def work(self, input_items, output_items):
        x = input_items[0]    # Input signal
        y = output_items[0]   # Output buffer
        
        # Calculate signal power (mean-square)
        signal_power = np.mean(np.abs(x**2))
        
        # Calculate required noise power based on snr
        noise_power = signal_power / 10**(self.snr/10)
        
        # Apply noise floor: use whichever is LARGER (max())
        # noise_power = max(noise_power, self.offset_power)
        
        # Generate Gaussian noise with calculated power
        # noise = self.rng.normal(0, np.sqrt(noise_power), len(x))
        
        # Generate noise
        noise = self.rng.normal(0, np.sqrt(noise_power), x.shape)
        
        # Add noise to signal
        y[:] = x + noise
        
        return len(y)