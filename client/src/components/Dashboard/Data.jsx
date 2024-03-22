import axios from 'axios';
import Chart from 'chart.js/auto';
import React, { useEffect, useState } from 'react';
import { Bar, Line } from 'react-chartjs-2';
import * as XLSX from 'xlsx';


import Loading from '../Loading/Loading';

const Data = () => {
    const [data, setData] = useState([]);
    const [accidentsPerDate, setAccidentsPerDate] = useState(null);
    const [accidentsPerLocation, setAccidentsPerLocation] = useState(null);
    const [loading, setLoading] = useState(true);
    Chart.defaults.font.size = 16;
    useEffect(() => {
        axios
            .get(process.env.REACT_APP_URL + '/falls')
            .then((response) => {
                setData(response.data);
                const accidentsByDate = {};
                const accidentsByLocation = {};
                data.forEach((accident) => {
                    const date = accident.accident_time.split(' ')[0];
                    if (accidentsByDate[date]) {
                        accidentsByDate[date]++;
                    } else {
                        accidentsByDate[date] = 1;
                    }

                    const location = `Lat: ${accident.latitude.toFixed(2)}, Long: ${accident.longitude.toFixed(2)}`;
                    if (accidentsByLocation[location]) {
                        accidentsByLocation[location]++;
                    } else {
                        accidentsByLocation[location] = 1;
                    }
                });
                const dateLabels = Object.keys(accidentsByDate);
                const dateValues = Object.values(accidentsByDate);
                const dateChartData = {
                    labels: dateLabels,
                    datasets: [
                        {
                            label: 'Number of Accidents',
                            data: dateValues,
                            backgroundColor: 'rgba(75, 192, 192, 0.6)',
                            borderColor: 'rgba(75, 192, 192, 1)',
                            borderWidth: 1,
                        },
                    ],
                };

                const locationLabels = Object.keys(accidentsByLocation);
                const locationValues = Object.values(accidentsByLocation);
                const locationChartData = {
                    labels: locationLabels,
                    datasets: [
                        {
                            label: 'Number of Accidents',
                            data: locationValues,
                            backgroundColor: 'rgba(54, 162, 235, 0.6)',
                            borderColor: 'rgba(54, 162, 235, 1)',
                            borderWidth: 1,
                        },
                    ],
                };

                setAccidentsPerDate(dateChartData);
                setAccidentsPerLocation(locationChartData);
                setLoading(false);
            })
            .catch((error) => {
                console.error('Error fetching data: ', error);
            });
    }, [data]);
    const handleDownloadExcel = () => {
        const workbook = XLSX.utils.book_new();
        const accidentsSheet = XLSX.utils.json_to_sheet(data);
        XLSX.utils.book_append_sheet(workbook, accidentsSheet, 'Accidents');
        const excelBuffer = XLSX.write(workbook, {
            bookType: 'xlsx',
            type: 'array',
        });
        saveAsExcelFile(excelBuffer, 'accidents.xlsx');
    };

    const saveAsExcelFile = (buffer, filename) => {
        const data = new Blob([buffer], { type: 'application/octet-stream' });
        const url = URL.createObjectURL(data);
        const link = document.createElement('a');
        link.href = url;
        link.setAttribute('download', filename);
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    };
    return (
        <div>
            {loading ? (
                <Loading />
            ) : <div>
                <button onClick={handleDownloadExcel} style={{
                    display: 'block',
                    margin: 'auto',
                    marginBottom: '20px',
                }}>Download Excel</button>
                <h1 style={{
                    textAlign: 'center',
                    marginTop: '20px',
                    marginBottom: '20px',
                }}>Number of Accidents per Date</h1>
                {accidentsPerDate && (
                    <Line
                        data={accidentsPerDate}
                        options={{
                            scales: {
                                x: {
                                    beginAtZero: true,
                                    stepSize: 1,
                                },
                                y: {
                                    beginAtZero: true,
                                    stepSize: 1,
                                },
                            },
                        }}
                    />
                )}
                <h1 style={{
                    textAlign: 'center',
                    marginTop: '20px',
                    marginBottom: '20px',
                }}>Number of Accidents per Location</h1>
                {accidentsPerLocation && (
                    <Bar
                        data={accidentsPerLocation}
                        options={{
                            scales: {
                                y: {
                                    beginAtZero: true,
                                    stepSize: 1,
                                },
                            },
                        }}
                    />
                )}
            </div>}
        </div>
    );
};

export default Data;