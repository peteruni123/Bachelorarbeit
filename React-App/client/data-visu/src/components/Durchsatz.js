import * as React from 'react';
import PropTypes from 'prop-types';
import CircularProgress from '@mui/material/CircularProgress';
import Typography from '@mui/material/Typography';
import Box from '@mui/material/Box';

export default function CircularProgressWithLabel(value) {
  return (
    <Box sx={{ position: 'relative', display: 'inline-flex' }}>
      <CircularProgress variant="determinate" value = {value} size={150} sx = {{marginTop: '10px'}}/>
      <Box
        sx={{
          top: '40px',
          left: 0,
          bottom: 0,
          right: 0,
          position: 'absolute',
          
          alignItems: 'center',
          justifyContent: 'center',
          
        }}
      >
        <Typography variant="h5" component="div" color="text.secondary">
          {`${Math.round((value/30)*100)/100}`}
          
        </Typography>

        <Typography variant="p" component="div" color="text.secondary">
          Wafer/Sekunde
        </Typography>
      </Box>
    </Box>
  );
}