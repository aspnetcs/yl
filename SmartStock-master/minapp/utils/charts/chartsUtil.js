import uCharts from '@/static/ucharts/u-charts.min.js';


// 封装 drawCharts 函数
export function drawChartsUtil(id, data, cWidth, cHeight) {
    const ctx = uni.createCanvasContext(id);
    const uChartsInstance = {};
    uChartsInstance[id] = new uCharts({
        type: "candle",
        context: ctx,
        width: cWidth,
        height: cHeight,
        categories: data.categories,
        series: data.series,
        animation: true,
        timing: "easeOut",
        duration: 1000,
        rotate: false,
        rotateLock: false,
        background: "#FFFFFF",
        color: ["#1890FF", "#91CB74", "#FAC858", "#EE6666", "#73C0DE", "#3CA272", "#FC8452", "#9A60B4", "#ea7ccc"],
        padding: [15, 15, 0, 15],
        fontSize: 13,
        fontColor: "#666666",
        dataLabel: false,
        dataPointShape: true,
        dataPointShapeType: "solid",
        touchMoveLimit: 60,
        enableScroll: false,
        enableMarkLine: false,
        legend: {
            show: true,
            position: "top",
            float: "center",
            padding: 1,
            margin: 1,
            backgroundColor: "rgba(0, 0, 0, 0)",
            borderColor: "rgba(0, 0, 0, 0)",
            borderWidth: 0,
            fontSize: 10,
            fontColor: "#666666",
            lineHeight: 11,
            hiddenColor: "#CECECE",
            itemGap: 10
        },
        xAxis: {
            disabled: true,
            labelCount: 4,
            itemCount: 30,
            disableGrid: true,
            gridColor: "#CCCCCC",
            gridType: "solid",
            dashLength: 4,
            scrollShow: true,
            scrollAlign: "right",
            scrollColor: "#A6A6A6",
            scrollBackgroundColor: "#EFEBEF",
            axisLine: true,
            axisLineColor: "#CCCCCC",
            calibration: false,
            fontColor: "#666666",
            fontSize: 10,
            lineHeight: 20,
            marginTop: 0,
            rotateLabel: true,
            rotateAngle: 45,
            boundaryGap: "center",
            splitNumber: 5,
            gridEval: 1,
            title: "",
            titleFontSize: 13,
            titleOffsetY: 0,
            titleOffsetX: 0,
            titleFontColor: "#666666",
            formatter: ""
        },
        yAxis: {
            disabled: false,
            disableGrid: false,
            splitNumber: 5,
            gridType: "solid",
            dashLength: 8,
            gridColor: "#CCCCCC",
            padding: 10,
            showTitle: false,
            data: []
        },
        extra: {
            candle: {
                color: {
                    upLine: "#f04864",
                    upFill: "#f04864",
                    downLine: "#2fc25b",
                    downFill: "#2fc25b"
                },
                average: {
                    show: true,
                    name: [
                        "MA5",
                        "MA10",
                        "MA30"
                    ],
                    day: [
                        5,
                        10,
                        20
                    ],
                    color: [
                        "#1890ff",
                        "#2fc25b",
                        "#facc14"
                    ]
                }
            },
            markLine: {
                type: "dash",
                dashLength: 5,
                data: [
                    {
                        value: 2150,
                        lineColor: "#f04864",
                        showLabel: true
                    },
                    {
                        value: 2350,
                        lineColor: "#f04864",
                        showLabel: true
                    }
                ]
            },
            tooltip: {
                showBox: true,
                showArrow: true,
                showCategory: false,
                borderWidth: 0,
                borderRadius: 0,
                borderColor: "#000000",
                borderOpacity: 0.7,
                bgColor: "#000000",
                bgOpacity: 0.7,
                gridType: "solid",
                dashLength: 4,
                gridColor: "#CCCCCC",
                boxPadding: 3,
                fontSize: 13,
                lineHeight: 20,
                fontColor: "#FFFFFF",
                legendShow: true,
                legendShape: "auto",
                splitLine: true,
                horizentalLine: false,
                xAxisLabel: false,
                yAxisLabel: false,
                labelBgColor: "#FFFFFF",
                labelBgOpacity: 0.7,
                labelFontColor: "#666666"
            }
        }
    });
    return uChartsInstance[id];
}