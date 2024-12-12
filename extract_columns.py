COLUMNS = ['RA', 'DEC', 'photo_z', 'MASS_BEST']
FILENAME = 'desidr9_galaxy_cspcat.fits'

import sys
from astropy.io import fits
import numpy as np
from astropy.table import Table

def extract_columns(input_file, output_file, columns, chunk_size=100000):
    """
    Efficiently extract specified columns from a large FITS table using memory mapping
    and writing directly to output FITS file.
    
    Parameters:
    -----------
    input_file : str
        Path to input FITS file
    output_file : str
        Path to output FITS file
    columns : list
        List of column names to extract
    chunk_size : int
        Number of rows to process at once
    """
    
    # Open the input file with memory mapping
    with fits.open(input_file, memmap=True) as hdul:
        # Get the table data
        data = hdul[1].data
        header = hdul[1].header
        
        # Get total number of rows
        nrows = len(data)
        
        # Verify all requested columns exist
        available_cols = data.names
        missing_cols = [col for col in columns if col not in available_cols]
        if missing_cols:
            raise ValueError(f"Columns not found in table: {missing_cols}")
        
        # Create column definitions for output file
        col_defs = []
        for col in columns:
            col_format = data.dtype[col].str
            col_defs.append(fits.Column(name=col, format=col_format))

        # Create new FITS file with the selected columns
        hdu = fits.BinTableHDU.from_columns(col_defs, nrows=nrows)
        
        # Copy relevant header keywords
        for key in header:
            if key not in ['NAXIS1', 'NAXIS2', 'TFIELDS']:
                try:
                    hdu.header[key] = header[key]
                except:
                    continue

        # Write the empty HDU to file
        hdu.writeto(output_file, overwrite=True)
        
        # Open the output file in update mode
        with fits.open(output_file, mode='update') as hdul_out:
            # Process the data in chunks
            for i in range(0, nrows, chunk_size):
                end_idx = min(i + chunk_size, nrows)
                
                # Write each column chunk by chunk
                for col in columns:
                    hdul_out[1].data[col][i:end_idx] = data[col][i:end_idx]
                
                # Print progress
                progress = (end_idx / nrows) * 100
                print(f"\rProgress: {progress:.1f}%", end='')
            
            # Ensure all data is written
            hdul_out.flush()

        print("\nExtraction complete!")

    # except Exception as e:
    #     print(f"Error: {str(e)}")
    #     sys.exit(1)
 
if __name__ == "__main__":
    extract_columns(FILENAME, 'data', COLUMNS)