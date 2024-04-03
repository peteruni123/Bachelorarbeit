import * as React from 'react';
import { BarChart } from '@mui/x-charts/BarChart';

export default function BasicBars({barchartdata, barchartbeschriftung}) {
  return (
    <BarChart
  xAxis={[
    {
      id: 'barCategories',
      data: barchartbeschriftung,
      scaleType: 'band',
    },
  ]}
  series={[
    {
      data: barchartdata,
    },
  ]}
  width={500}
  height={300}
/>
  );
}