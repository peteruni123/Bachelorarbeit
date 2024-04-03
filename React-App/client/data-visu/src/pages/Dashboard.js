import AppBar from '../components/AppBar2'
import Drawer from '../components/Drawer2';
import * as React from 'react';
import Box from '@mui/material/Box';
import Container from '@mui/material/Container';
import Grid from '@mui/material/Grid';
import Paper from '@mui/material/Paper';
import Toolbar from '@mui/material/Toolbar';
import { styled, createTheme, ThemeProvider } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import Title from '../components/Title';
import BarChart from '../components/BarChart';
import BasicPie from '../components/PieChart';
import CircularProgressWithLabel from '../components/Durchsatz';
import axios from 'axios'



//Das ist die Dashboard Seite hier werden Prozessdaten visualisiert die sich auf die Gesamte Anlage beziehen
const Dashboard = () => {

    //Benötigte UseStates
    const [open, setOpen] = React.useState(false);
    const [page, setPage] = React.useState("Dashboard");
    const [produktionsdaten, setProduktionsdaten] = React.useState(null)
    const [barchartdata, setBarchardata] = React.useState([0,0,0,0,0,0])
    const [barchartbeschriftung, setBarchartbeschriftung] = React.useState(['bar A', 'bar B', 'bar C','bar d', 'bar e', 'bar f'])
    const [piechartdata, setPiechardata] = React.useState([0,0,0,0,0,0,0])
    const [piechartbeschriftung, setPiechartbeschriftung] = React.useState(['DarkDarkblue', 'Darkblue', 'Lightblue','LightLightblue', 'Dark-Mixed', 'Light-Mixed','No fit'])
    const [value, setValue] = React.useState(0)
    const defaultTheme = createTheme();

    //Hier wird aus den Produktionsdaten der Waferdurchsatz in den letzten 30 Sekunden berechnet
    const DurchsatzBerechnung = () =>{
        const date = new Date()
        var count = 0
        for(let item in produktionsdaten){
            var date_db = new Date(produktionsdaten[item].Zeitstempel)
            var diffTime = Math.abs(date - date_db);
            var diffSekunden = (diffTime/ (1000))

            if(diffSekunden <= 30){
                count = count + 1
            }
        }
        setValue(count)
    }

    //Hier wird aus den Produktionsdaten die Anzahl der analysierten Wafer nach Stunden aufgeteilt
    const BarChartBerechnungen = () => {
        const date = new Date()
        const aktuelle_stunde = date.getHours()
        let Data_Array = [0,0,0,0,0,0]
        let Beschriftungs_array = ['bar A', 'bar B', 'bar C','bar d', 'bar e', 'bar f']
        const Zeitraum = Data_Array.length
        const differenz = aktuelle_stunde - Zeitraum 
        for(let v in Data_Array){
            var Zeit1 = aktuelle_stunde - v 
            var Zeit2 = Zeit1 + 1
            Beschriftungs_array[aktuelle_stunde-differenz - v -1] = Zeit1.toString() + '-' + Zeit2.toString()
        }
        setBarchartbeschriftung(Beschriftungs_array)
        
        for(let item in produktionsdaten){
            var date_db = new Date(produktionsdaten[item].Zeitstempel)
            var date_db_hr = date_db.getHours()
            for(let i in Data_Array){
                if(date_db_hr  === aktuelle_stunde - i){
                    Data_Array[aktuelle_stunde-differenz- i -1] = Data_Array[aktuelle_stunde-differenz- i -1] + 1
                }
            }
        }
        setBarchardata(Data_Array)
    }

    //Hier werden die Analyse-Ergebnisse der letzten Stunde nach Kategorie sortiert
    const PieChartBerechnung = () => {
        const date = new Date()
        let Data_Array = [0,0,0,0,0,0,0]

        for(let item in produktionsdaten){
            var date_db = new Date(produktionsdaten[item].Zeitstempel)
            var diffTime = Math.abs(date - date_db);
            var diffMinutes = (diffTime/ (1000*60))
            if (diffMinutes < 60){
                if (produktionsdaten[item].Ergebnis === 'Ddb'){
                    Data_Array[0] = Data_Array[0] + 1
                }
                else if (produktionsdaten[item].Ergebnis === 'Db'){
                    Data_Array[1] = Data_Array[1] + 1
                }
                else if (produktionsdaten[item].Ergebnis === 'Lb'){
                    Data_Array[2] = Data_Array[2] + 1
                }
                else if (produktionsdaten[item].Ergebnis === 'Llb'){
                    Data_Array[3] = Data_Array[3] + 1
                }
                else if (produktionsdaten[item].Ergebnis === 'Md'){
                    Data_Array[4] = Data_Array[4] + 1
                }
                else if (produktionsdaten[item].Ergebnis === 'Ml'){
                    Data_Array[5] = Data_Array[5] + 1
                }
                else{
                    Data_Array[6] = Data_Array[6] + 1
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
                    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
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
                                        <BarChart barchartdata = {barchartdata} barchartbeschriftung ={barchartbeschriftung}/>
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
                                        {BasicPie(piechartbeschriftung, piechartdata)}

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
                                        {CircularProgressWithLabel(value)}

                                </Paper>
                            </Grid>
                                
                            
                        </Grid>
                    </Container>

                </Box>
            </Box>
        </ThemeProvider>
    );
}
    
export default Dashboard;