import AppBar from '../components/AppBar2'
import Drawer from '../components/Drawer2';
import * as React from 'react';
import Box from '@mui/material/Box';
import { styled, createTheme, ThemeProvider } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import Grid from '@mui/material/Grid';
import Paper from '@mui/material/Paper';
import Toolbar from '@mui/material/Toolbar';
import Title from '../components/Title';
import Slider from '@mui/material/Slider';
import Typography from '@mui/material/Typography';
import axios from 'axios'
import Container from '@mui/material/Container';
import BarChart from '../components/BarChart';
import BasicPie from '../components/PieChart';
import CircularProgressWithLabel from '../components/Durchsatz';


//Das ist die Details Seite hier werden wie im Dashboard Produktionsdaten visualisiert mit dem Unterschied,
// dass sie hier nach den Kameras aufgeteilt sind

const Details = () => {
    //Benötigte UseStates
    const [open, setOpen] = React.useState(false);
    const [page, setPage] = React.useState("Details");
    const [params, setParams] = React.useState(null);
    const defaultTheme = createTheme();
    const [produktionsdaten, setProduktionsdaten] = React.useState(null)
    const [barchartdata, setBarchardata] = React.useState(null)
    const [barchartbeschriftung, setBarchartbeschriftung] = React.useState(['bar A', 'bar B', 'bar C','bar d', 'bar e', 'bar f'])
    const [piechartdata, setPiechardata] = React.useState(null)
    const [piechartbeschriftung, setPiechartbeschriftung] = React.useState(['DarkDarkblue', 'Darkblue', 'Lightblue','LightLightblue', 'Dark-Mixed', 'Light-Mixed','No fit'])
    const [value, setValue] = React.useState([0,0,0])
    
    //Hier wird aus den Produktionsdaten der Waferdurchsatz pro Kamera in den letzten 30 Sekunden berechnet
    const DurchsatzBerechnung = () =>{
        const date = new Date()
        let count_arr = []
        for (let kamera in params)
            count_arr.push(0)

        for(let item in produktionsdaten){
            var date_db = new Date(produktionsdaten[item].Zeitstempel)
            var diffTime = Math.abs(date - date_db);
            var diffSekunden = (diffTime/ (1000))

            if(diffSekunden <= 30){
                var index = 0
                    for (let kamera in count_arr){
                        if (params[kamera].Name === produktionsdaten[item].Kameraname){
                            index = kamera
                        }
                    }
                count_arr[index] = count_arr[index] + 1
            }
        }
        setValue(count_arr)
    }

    //Hier wird aus den Produktionsdaten die Anzahl der analysierten Wafer nach Stunden und Kamera aufgeteilt
    const BarChartBerechnungen = () => {
        const date = new Date()
        const aktuelle_stunde = date.getHours()
        
        let Data_Array = []
        for (let kamera in params)
            Data_Array.push([0,0,0,0,0,0])

        let Beschriftungs_array = ['bar A', 'bar B', 'bar C','bar d', 'bar e', 'bar f']
        const Zeitraum = Data_Array[0].length
        const differenz = aktuelle_stunde - Zeitraum 
        for(let v in Data_Array[0]){
            var Zeit1 = aktuelle_stunde - v 
            var Zeit2 = Zeit1 + 1
            Beschriftungs_array[aktuelle_stunde-differenz - v -1] = Zeit1.toString() + '-' + Zeit2.toString()
        }
        setBarchartbeschriftung(Beschriftungs_array)
        
        for(let item in produktionsdaten){
            var date_db = new Date(produktionsdaten[item].Zeitstempel)
            var date_db_hr = date_db.getHours()
            for(let i in Data_Array[0]){
                if(date_db_hr  === aktuelle_stunde - i){
                    var index = 0
                    for (let kamera in Data_Array){
                        if (params[kamera].Name === produktionsdaten[item].Kameraname){
                            index = kamera
                        }
                    }
                    Data_Array[index][aktuelle_stunde-differenz- i -1] = Data_Array[index][aktuelle_stunde-differenz- i -1] + 1
                }
            }
        }
        setBarchardata(Data_Array)
    }

    //Hier werden die Analyse-Ergebnisse in der letzten Stunde nach Kategorie und Kamera sortiert
    const PieChartBerechnung = () => {
        const date = new Date()
        let Data_Array = []
        for (let kamera in params)
            Data_Array.push([params[kamera].Name,[0,0,0,0,0,0,0]])

        for(let item in produktionsdaten){
            var date_db = new Date(produktionsdaten[item].Zeitstempel)
            var diffTime = Math.abs(date - date_db);
            var diffMinutes = (diffTime/ (1000*60))
        
            if (diffMinutes < 60){
                var index = 0 
                for(let kamera in Data_Array){
                    if(Data_Array[kamera][0] === produktionsdaten[item].Kameraname){
                        index = kamera
                    }

                }
                if (produktionsdaten[item].Ergebnis === 'Ddb'){
                    Data_Array[index][1][0] = Data_Array[index][0] + 1
                }
                else if (produktionsdaten[item].Ergebnis === 'Db'){
                    Data_Array[index][1][1] = Data_Array[index][1][1] + 1
                }
                else if (produktionsdaten[item].Ergebnis === 'Lb'){
                    Data_Array[index][1][2] = Data_Array[index][1][2] + 1
                }
                else if (produktionsdaten[item].Ergebnis === 'Llb'){
                    Data_Array[index][1][3] = Data_Array[index][1][3] + 1
                }
                else if (produktionsdaten[item].Ergebnis === 'Md'){
                    Data_Array[index][1][4] = Data_Array[index][1][4] + 1
                }
                else if (produktionsdaten[item].Ergebnis === 'Ml'){
                    Data_Array[index][1][5] = Data_Array[index][1][5] + 1
                }
                else{
                    Data_Array[index][1][6] = Data_Array[index][1][6] + 1
                }
            }
        }
        setPiechardata(Data_Array)
    }

    //Anfrage an das Backend zum erlangen der Produktionsdaten und Aufruf der Berechnungsfunktionen
    const GetProduktionData = async(date) =>{
        try{
            const response = await axios.get('http://localhost:8000/getProduktionData',{})
            setProduktionsdaten(response.data)
            BarChartBerechnungen()
            PieChartBerechnung()
            DurchsatzBerechnung()
        }
        catch(error){
            console.log(error)
        }
    } 

    //Wird ab Aufruf der Seite zyklisch alle 2 Sekunden ausgeführt
    React.useEffect(() => {
        const interval = setInterval(() => {
          GetProduktionData(new Date())
        }, 2000);
    
        return () => clearInterval(interval);
      }, [GetProduktionData]);

    //Anfrage an das Backend um die Paramter und somit indirekt die Anazhl der Kameras zu erlangen
    const GetParams = async () => {
        try {
            const response = await axios.get('http://localhost:8000/getParamData', {})
            setParams(response.data)
            
        } catch (error) {
            console.log(error)
        }
    }

    //Wird bei dem neuladen dieser Seite aufgerufen
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
                    height: '100vh',
                    overflow: 'auto',
                }}
                >
                    <Toolbar />
                    {params?.map((param, _index) => (
                        <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
                            <Typography component="h4" variant="h4" color="primary" gutterBottom>
                                Daten zu {param?.Name}
                            </Typography>
                            <Grid container spacing={3}>
                            <Grid item xs={12} md={12} lg={12}>
                                <Paper
                                        
                                    sx={{
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
                                        <Title>Anzahl Wafer nach Stunden</Title>
                                        {barchartdata!= null ? <BarChart barchartdata = {barchartdata[_index]} barchartbeschriftung ={barchartbeschriftung}/> : <BarChart barchartdata = {[0,0,0,0,0,0]} barchartbeschriftung ={barchartbeschriftung}/>}
                                </Paper>
                            </Grid>
                            <Grid item xs={8} md={8} lg={8}>
                                <Paper
                                        
                                    sx={{
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
                                        <Title>Ergebnisse der Farbanalyse in der letzten Stunde</Title>
                                        
                                        { piechartdata!= null ? BasicPie(piechartbeschriftung, piechartdata[_index][1]) : BasicPie(piechartbeschriftung, [0,0,0,0,0,0,0])}

                                </Paper>
                            </Grid>
                            <Grid item xs={4} md={4} lg={4}>
                                <Paper
                                        
                                    sx={{
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
                                        <Title>Wafer Durchsatz in den letzten 30 Sekunden</Title>
                                        {CircularProgressWithLabel(value[_index])}

                                </Paper>
                            </Grid>
                        
                            </Grid>
                            </Container>
                            ))}

                </Box>
            </Box>
        </ThemeProvider>
    );
}
    
export default Details;