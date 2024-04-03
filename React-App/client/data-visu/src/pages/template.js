import AppBar from '../components/AppBar2'
import Drawer from '../components/Drawer2';
import * as React from 'react';
import Box from '@mui/material/Box';
import { styled, createTheme, ThemeProvider } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import Container from '@mui/material/Container';
import Grid from '@mui/material/Grid';
import Paper from '@mui/material/Paper';
import Toolbar from '@mui/material/Toolbar';


//Das ist mein Base Template auf dem alle Pages aufbauen werden
const Test = () => {

    const [open, setOpen] = React.useState(false);
    const [page, setPage] = React.useState("test");
    const defaultTheme = createTheme();

    return (
        
         <ThemeProvider theme={defaultTheme}>
            <Box sx={{ display: 'flex' }}>
                <CssBaseline />
                <AppBar open ={open} setOpen = {setOpen} page = {page}/>
                <Drawer open ={open} setOpen = {setOpen} page = {page}/>
                <Box
                component="main"
                sx={{
                    backgroundColor: (theme) =>
                    theme.palette.mode === 'light'
                        ? theme.palette.grey[100]
                        : theme.palette.grey[900],
                    flexGrow: 1,
                    height: '100vh',
                    overflow: 'auto',
                }}
                >
            <Toolbar />
            <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
            <Grid columns={24} container spacing={3}>
              {/* Chart */}
              <Grid  item xs={12} md={8} lg={6}>
                <Paper
                  sx={{
                    p: 2,
                    display: 'flex',
                    flexDirection: 'column',
                    height: 240,
                  }}
                >
                  
                </Paper>
              </Grid>
              {/* Recent Deposits */}
              <Grid item xs={12} md={4} lg={6}>
                <Paper
                  sx={{
                    p: 2,
                    display: 'flex',
                    flexDirection: 'column',
                    height: 240,
                  }}
                >
                  
                </Paper>
              </Grid>
              {/* Recent Orders */}
              <Grid item xs={12}>
                <Paper sx={{ p: 2, display: 'flex', flexDirection: 'column', height:'240px' }}>
                  
                </Paper>
              </Grid>
            </Grid>
           
          </Container>

                </Box>
            </Box>
        </ThemeProvider>
    );
}
    
export default Test;