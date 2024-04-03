import * as React from 'react';
import { PieChart } from '@mui/x-charts/PieChart';

export default function BasicPie(piechartbeschriftung, piechartdata) {
  return (
    <PieChart
    colors={['#00008b', '#0F52BA', '#008ECC', '#7EF9FF', 'black', 'gray', 'red']}
      series={[
        {
          data: [
            { id: 0, value: piechartdata[0], label: piechartbeschriftung[0] },
            { id: 1, value: piechartdata[1], label: piechartbeschriftung[1] },
            { id: 2, value: piechartdata[2], label: piechartbeschriftung[2] },
            { id: 3, value: piechartdata[3], label: piechartbeschriftung[3] },
            { id: 4, value: piechartdata[4], label: piechartbeschriftung[4] },
            { id: 5, value: piechartdata[5], label: piechartbeschriftung[5] },
            { id: 6, value: piechartdata[6], label: piechartbeschriftung[6] }
            
          ],
        },
      ]}
      width={600}
      height={200}
    />
  );
}