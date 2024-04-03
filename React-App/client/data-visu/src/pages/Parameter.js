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
import Title from '../components/Title';
import Slider from '@mui/material/Slider';
import Typography from '@mui/material/Typography';
import axios from 'axios'
import zIndex from '@mui/material/styles/zIndex';
import Button from '@mui/material/Button';



//Auf dieser Seite werden die Parameter angezeigt und die Werte dieser können mit Hilfe von Slidern verändert werden
const Parameter = () => {

    //Benötigte UseStates
    const [open, setOpen] = React.useState(false);
    const [page, setPage] = React.useState("Parameter");
    const [params, setParams] = React.useState(null);

    //Theme auswählen
    const defaultTheme = createTheme();
    
    //Wird aufgerufen wenn der Slider bewegt wird und schreibt neuen Wert in params UseState
    const handleSliderChange = (e,index) => {
        setParams(params.map(param => {
            if (param.Indizes === index) {
              // Create a *new* object with changes
              return { ...param, Value: e.target.value.toString() };
            } else {
              // No changes
              return param;
            }
          }));
      };

    
    //Fordert die Parameter-Daten aus dem Backend an
    const GetParams = async () => {
        try {
            const response = await axios.get('http://localhost:8000/getParamData', {})
            console.log("here")
            setParams(response.data)
            console.log(response.data)
            
        } catch (error) {
            console.log(error)
        }
    }
    
    //Fordert das Backend auf die neuen Parameterdaten in die SPS zu schreiben
    const ParameterSchreiben = async () => {
        try {
            const response = await axios.put('http://localhost:8000/sendParamData', {params})
            
        } catch (error) {
            console.log(error)
        }
    }
        
    
    //Wird beim Laden der Seite aufgerufen
    React.useEffect(() => {
        GetParams()
         
    },[]) 


    //html output wird in Abhängigkeit der Daten gerendert und aktualisiert
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
                    height: '200vh',
                    overflow: 'auto',
                }}
                >
                    {/* Seitenspezifischer Content */}
                <Toolbar />
                <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
                    <Grid container spacing={3}>
                            {/* Chart */}
                            <Grid item xs={12} md={8} lg={12}>
                                <Paper
                                    
                                    sx={{
                                        width: '100%',
                                        p: 2,
                                        display: 'flex',
                                        flexDirection: 'column',
                                        height: 'auto',
                                        alignItems: 'center',
                                        textAlign: "center",
                                        verticalAlign: "middle",
                                        justifyContent: "center",
                                    }}
                                >
                                    <Title>Warte-Timer</Title>
                                    <Typography id="input-slider" gutterBottom>
                                        Hier kann für jeden Bahn die Wartezeit zwischen den Waferinspektionen eingestellt werden.
                                        Eine geringe Wartezeit führt zu einer erhöhten Taktfrequenz auf der ausgewählten Bahn.
                                    </Typography>
                                    {params?.map((param, _index) => (
                                    <Grid container spacing={2} alignItems="center"
                                    key={_index}
                                     sx ={{marginTop:'20px',
                                        width: '600px',
                                        }} >

                                        <Grid item sx={{ width:'200px' }}>
                                            <Box component="div" sx={{
                                                width:'50px', 
                                                display: 'inline',
                                                p: 1,
                                                m: 1,
                                                bgcolor: (theme) => (theme.palette.mode === 'dark' ? '#101010' : '#fff'),
                                                color: (theme) =>
                                                theme.palette.mode === 'dark' ? 'grey.300' : 'grey.800',
                                                border: '1px solid',
                                                borderColor: (theme) =>
                                                theme.palette.mode === 'dark' ? 'grey.800' : 'grey.300',
                                                borderRadius: 2,
                                                fontSize: '0.875rem',
                                                fontWeight: '700',}}>
                                                    {param?.Name}
                                            </Box>
                                        </Grid>    
                                        <Grid item xs
                                            sx = {{
                                                width: '200px'
                 
                                            }}>
                                            <Slider
                                                value={typeof parseInt(params[_index].Value) === 'number' ? parseInt(params[_index].Value) : 0}
                                                onChange={(e) => handleSliderChange(e,param.Indizes)}
                                                aria-labelledby="input-slider"
                                                valueLabelDisplay="auto"
                                                step ={100}
                                                min ={0}
                                                max ={10000}
                                                color = "secondary"
                                
                                            />
                                        </Grid>
                                        <Grid item sx={{ width:'150px' }}>
                                        <Box component="div"
                                            sx={{
                                            width:'150px', 
                                            display: 'inline',
                                            p: 1,
                                            m: 1,
                                            bgcolor: (theme) => (theme.palette.mode === 'dark' ? '#101010' : '#fff'),
                                            color: (theme) =>
                                              theme.palette.mode === 'dark' ? 'grey.300' : 'grey.800',
                                            border: '1px solid',
                                            borderColor: (theme) =>
                                              theme.palette.mode === 'dark' ? 'grey.800' : 'grey.300',
                                            borderRadius: 2,
                                            fontSize: '0.875rem',
                                            fontWeight: '700',}}>
                                                {params[_index].Value} ms</Box>
                                        </Grid>
                                    </Grid>
                                    ))}
                                    <Button variant="contained" color="secondary" sx = {{ marginTop: '50px'}} onClick={ParameterSchreiben} >
                                         Werte in die SPS schreiben
                                         </Button>

                                
                            
                                </Paper>
                            </Grid>
                        </Grid>
                    </Container>


                </Box>
            </Box>
        </ThemeProvider>
    );
}
    
export default Parameter;