var endpointRunSim = '/api/sim/runsim';
var endpointErlangPdf = '/api/sim/erlangpdf';
var endpointSaveSim = '/api/sim/'
//var chartInputLos;
var chartInputCat1;
var chartInputCat2;
var chartInputCat3;
var chartOutputMedication;
var chartOutputResources;
var chartOutputConsultations
const csrftoken = $("[name=csrfmiddlewaretoken]").val();

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});



$(document).ready(function() {


    // Gather all form data
    var formData = $('#formInput1, #formInput2, #hiddenInputForm').serialize()

    // Disable all inputs while simulation is running
    $('#inputdiv input').each(function() {
        $(this).prop( "disabled", true );
    })

    // Show loading div
    $(".loading-div").each(function() {
        $(this).show()
    })

    // Draw input distribution
    draw_input_charts(formData)
    outputFormData = JSON.parse($('#id_output').val())
    if ($.isEmptyObject(outputFormData)) {
        draw_output_charts(formData)
    }
    else {
        draw_output_charts_initialized(outputFormData)
    }



    // Detect changes in input form
    $('#inputdiv input').change(function() {

        // Remove "simulation from ..." text
        $('#id_simFrom').text('')

        // Reset save window
        $('.success-div, .danger-div').each(function() {
            $(this).hide()
        })
        $('#save_sim_btn').show()
        $('#id_formDiv').show()


        // First cases represent toggle switch
        if ($(this).attr('id') == 'id_switchLos') {
            var chartDataId = []
            chartDataId.push(get_chart_data_id(document.getElementById('lowRiskLos')))
            chartDataId.push(get_chart_data_id(document.getElementById('medRiskLos')))
            chartDataId.push(get_chart_data_id(document.getElementById('highRiskLos')))
            if (chartInputLos.data.datasets[chartDataId[0]]['hidden']) {
                for (var i=0;i<chartDataId.length;i++) {
                    chartInputLos.data.datasets[chartDataId[i]]['hidden'] = false
                }
            }
            else {
                for (var i=0;i<chartDataId.length;i++) {
                    chartInputLos.data.datasets[chartDataId[i]]['hidden'] = true
                }
            }
            chartInputLos.update()

        }
        else if ($(this).attr('id') == 'id_switchIcuLos') {
            var chartDataId = []
            chartDataId.push(get_chart_data_id(document.getElementById('lowRiskIcuLos')))
            chartDataId.push(get_chart_data_id(document.getElementById('medRiskIcuLos')))
            chartDataId.push(get_chart_data_id(document.getElementById('highRiskIcuLos')))
            if (chartInputLos.data.datasets[chartDataId[0]]['hidden']) {
                for (var i=0;i<chartDataId.length;i++) {
                    chartInputLos.data.datasets[chartDataId[i]]['hidden'] = false
                }
            }
            else {
                for (var i=0;i<chartDataId.length;i++) {
                    chartInputLos.data.datasets[chartDataId[i]]['hidden'] = true
                }
            }
            chartInputLos.update()
        }
        else if ($(this).attr('id') == 'id_switchVentLos') {
            var chartDataId = []
            chartDataId.push(get_chart_data_id(document.getElementById('lowRiskVentLos')))
            chartDataId.push(get_chart_data_id(document.getElementById('medRiskVentLos')))
            chartDataId.push(get_chart_data_id(document.getElementById('highRiskVentLos')))
            if (chartInputLos.data.datasets[chartDataId[0]]['hidden']) {
                for (var i=0;i<chartDataId.length;i++) {
                    chartInputLos.data.datasets[chartDataId[i]]['hidden'] = false
                }
            }
            else {
                for (var i=0;i<chartDataId.length;i++) {
                    chartInputLos.data.datasets[chartDataId[i]]['hidden'] = true
                }
            }
            chartInputLos.update()

        }

        // This is for a change for all other input values
        else {
            $('#id_divSimDate').html("")
            formData = $('#formInput1, #formInput2, #hiddenInputForm').serialize()


            // Disable all inputs while simulation is running
            $('#inputdiv input').each(function() {
                $(this).prop( "disabled", true );
            })

            // Show loading div
            $(".loading-div").each(function() {
                $(this).show()
            })

            // Check if element is part of formInput2
            if ($(this).closest("form").attr('id') == 'formInput2') {
                var mean = [parseInt($(this).val(), 10)]
                chartDataId = get_chart_data_id(this)
                update_input_charts(formData, chartDataId, mean)
                }

            // Update output data
            update_output_charts(formData)
        }
    });

    // When save button clicked
    $("#save_sim_btn").click(function(e) {
        $('#dropdownSaveSim').dropdown('toggle')
        e.preventDefault();
        $.ajax({
            type: "POST",
            url: endpointSaveSim,
            data: $('#formInput1, #formInput2, #saveForm, #outputForm, #hiddenInputForm').serialize(),
            success: function(result) {
                $('#save_sim_btn').hide()
                $('#id_formDiv').hide()
                $('.danger-div').each(function() {
                    $(this).hide()
                })
                $('.success-div').each(function() {
                    $(this).show()
                })
                var date = new Date();
                // Add "simulation from ..." text
                $("#saveForm")[0].reset();
                $('#id_simFrom').text('Simulation from now')
            },
            error: function(xhr, status, error) {
                $('.danger-div').each(function() {
                    console.log(xhr.responseText)
                    var err = (xhr.responseText);
                    $(this).html(err.Message)
                    $(this).show()
                    setTimeout(function() {
                        $('.danger-div').each(function() {$(this).slideUp('slow')}) //$(this).hide()
                        }, 5000);
                })
            }
        });
    });


});

// Enables all input forms and hides loading div after graphs have been updated
$(document).ajaxStop(function() {
    $('#inputdiv input').each(function() {
        $(this).prop( "disabled", false );
    })
    $(".loading-div").each(function() {
        $(this).hide()
    })
});

$('#id_navItemHome').addClass("active");

// ---------- functions ------------

function update_input_charts(formData, chartDataId, mean) {
    $.ajax({
        method: "GET",
        url: endpointErlangPdf,
        data: formData,
        success: function (data) {
            var subId = get_subChart_data_id(document.getElementById(get_form_id(chartDataId)))
            if (get_form_id(chartDataId).indexOf('cat1')>0) {
                chartInputCat1.data.datasets[subId].data = data['pdf'][mean]
                chartInputCat1.update()
            }
            else if (get_form_id(chartDataId).indexOf('cat2')>0) {
                chartInputCat2.data.datasets[subId].data = data['pdf'][mean]
                chartInputCat2.update()
            }
            else {
                chartInputCat3.data.datasets[subId].data = data['pdf'][mean]
                chartInputCat3.update()
            }
        },
        error: function (error_data) {
          console.log("error")
          console.log(error_data)
        }
    })

}

function update_output_charts(formData) {
    $.ajax({
        method: "GET",
        url: endpointRunSim,
        data: formData,
        success: function (data) {
          $('#id_output').val(JSON.stringify(data))
          time = data['days']
          var dataMedication = []
          var dataResources = []
          var dataConsultations = [{
            'data': data['consultations'],
            'backgroundColor': '#1c73b1'
          }]
          $.each(data['medication'], function(k, v){
            dataMedication.push({})
            dataMedication[dataMedication.length-1]['label'] = k
            dataMedication[dataMedication.length-1]['data'] = v
            dataMedication[dataMedication.length-1]['fill'] = false
          })
          $.each(data['resources'], function(k, v){
            dataResources.push({})
            dataResources[dataResources.length-1]['label'] = k
            dataResources[dataResources.length-1]['data'] = v
            dataResources[dataResources.length-1]['fill'] = false
          })
          chartOutputMedication.data.labels = time
          chartOutputMedication.data.datasets = dataMedication
          chartOutputMedication.update()

          chartOutputResources.data.labels = time
          chartOutputResources.data.datasets = dataResources
          chartOutputResources.update()

          chartOutputConsultations.data.labels = time
          chartOutputConsultations.data.datasets = dataConsultations
          chartOutputConsultations.update()
        },
        error: function (error_data) {
          $('#id_output').val(JSON.stringify(error_data))
          console.log("error")
          console.log(error_data)
        }
    });
}

function draw_input_charts(formData) {
    var mean = []
    var dataLos = []
    $('#formInput2 input').each(function() {
        chartDataId = get_chart_data_id(this)  //  represents index of data in list
        mean[chartDataId] = parseInt($(this).val(), 10)
    });
    $.ajax({
                method: "GET",
                url: endpointErlangPdf,
                data: formData,
                success: function (data) {
                    time = data.Days
                    for (i=0;i<mean.length;i++) {
                        dataLos[i] = {}
                        dataLos[i]['label'] = 'test'
                        dataLos[i]['data'] = data['pdf'][mean[i]]
                        dataLos[i]['fill'] = false
                        dataLos[i]['pointRadius'] = 0
                        formId = get_form_id(i)
                        if (formId.indexOf("Icu")>=0) {
                            dataLos[i]['borderColor'] = '#b4d4da'
//                            dataLos[i]['backgroundColor'] = '#5cb85c'
                        }
                        else if (formId.indexOf("Ecmo")>=0) {
                            dataLos[i]['borderColor'] = '#67add4'
//                            dataLos[i]['borderDash'] = [15,5]
                            dataLos[i]['backgroundColor'] = '#f0ad4e'
                        }
                        else if (formId.indexOf("Vent")>=0) {
                            dataLos[i]['borderColor'] = '#1c73b1'
//                            dataLos[i]['borderDash'] = [10,10]
//                            dataLos[i]['backgroundColor'] = '#f0ad4e'
                        }
                        else if (formId.indexOf("Dialysis")>=0) {
                            dataLos[i]['borderColor'] = '#26456e'
//                            dataLos[i]['borderDash'] = [2,2]
//                            dataLos[i]['backgroundColor'] = '#f0ad4e'
                        }

//                        if (formId.indexOf("Icu")>=0) {
//                            dataLos[i]['borderDash'] = [10,5]
//                        }
//                        else if (formId.indexOf("Vent")>=0) {
//                            dataLos[i]['borderDash'] = [1,1]
//                        }
                    }

//                    ctx = document.getElementById('chartInputLos')
                    ctxCat1 = document.getElementById('chartInput-cat1')
                    ctxCat2 = document.getElementById('chartInput-cat2')
                    ctxCat3 = document.getElementById('chartInput-cat3')
//                    chartInputLos = set_chart(ctx, dataLos, 'line', '', false, false)//'brewer.DarkTwo5')

                    dataCat1 = [];
                    dataCat1[get_subChart_data_id(document.getElementById('id_daysIcu_cat1'))] =
                        dataLos[get_chart_data_id(document.getElementById('id_daysIcu_cat1'))];
                    dataCat1[get_subChart_data_id(document.getElementById('id_daysEcmo_cat1'))] =
                        dataLos[get_chart_data_id(document.getElementById('id_daysEcmo_cat1'))];
                    dataCat1[get_subChart_data_id(document.getElementById('id_daysDialysis_cat1'))] =
                        dataLos[get_chart_data_id(document.getElementById('id_daysDialysis_cat1'))];
                    chartInputCat1 = set_chart(ctxCat1, dataCat1, 'line', '', false, false)//'brewer.DarkTwo5')

                    dataCat2 = [];
                    dataCat2[get_subChart_data_id(document.getElementById('id_daysIcu_cat2'))] =
                        dataLos[get_chart_data_id(document.getElementById('id_daysIcu_cat2'))];
                    dataCat2[get_subChart_data_id(document.getElementById('id_daysVent_cat2'))] =
                        dataLos[get_chart_data_id(document.getElementById('id_daysVent_cat2'))];
                    dataCat2[get_subChart_data_id(document.getElementById('id_daysDialysis_cat2'))] =
                        dataLos[get_chart_data_id(document.getElementById('id_daysDialysis_cat2'))];
                    chartInputCat2 = set_chart(ctxCat2, dataCat2, 'line', '', false, false)//'brewer.DarkTwo5')

                    dataCat3 = [];
                    dataCat3[get_subChart_data_id(document.getElementById('id_daysIcu_cat3'))] =
                        dataLos[get_chart_data_id(document.getElementById('id_daysIcu_cat3'))];
                    dataCat3[get_subChart_data_id(document.getElementById('id_daysDialysis_cat3'))] =
                        dataLos[get_chart_data_id(document.getElementById('id_daysDialysis_cat3'))];
                    chartInputCat3 = set_chart(ctxCat3, dataCat3, 'line', '', false, false)//'brewer.DarkTwo5')

                },
                error: function (error_data) {
                  console.log("error")
                  console.log(error_data)
                }
            })

}

function get_chart_data_id(inputForm) {
    switch (inputForm.id) {
        case 'id_daysIcu_cat1':
            return 0
        case 'id_daysIcu_cat2':
            return 1
        case 'id_daysIcu_cat3':
            return 2
        case 'id_daysEcmo_cat1':
            return 3
        case 'id_daysEcmo_cat2':
            return 4
        case 'id_daysEcmo_cat3':
            return 5
        case 'id_daysVent_cat1':
            return 6
        case 'id_daysVent_cat2':
            return 7
        case 'id_daysVent_cat3':
            return 8
        case 'id_daysDialysis_cat1':
            return 9
        case 'id_daysDialysis_cat2':
            return 10
        case 'id_daysDialysis_cat3':
            return 11
    }
}

function get_subChart_data_id(inputForm) {
    switch (inputForm.id) {
        case 'id_daysIcu_cat1':
            return 0
        case 'id_daysIcu_cat2':
            return 0
        case 'id_daysIcu_cat3':
            return 0
        case 'id_daysEcmo_cat1':
            return 1
        case 'id_daysEcmo_cat2':
            return -1
        case 'id_daysEcmo_cat3':
            return -1
        case 'id_daysVent_cat1':
            return -1
        case 'id_daysVent_cat2':
            return 1
        case 'id_daysVent_cat3':
            return -1
        case 'id_daysDialysis_cat1':
            return 2
        case 'id_daysDialysis_cat2':
            return 2
        case 'id_daysDialysis_cat3':
            return 1
    }
}

function get_form_id(chartDataId) {
    switch (chartDataId) {
        case 0:
            return 'id_daysIcu_cat1'
        case 1:
            return 'id_daysIcu_cat2'
        case 2:
            return 'id_daysIcu_cat3'
        case 3:
            return 'id_daysEcmo_cat1'
        case 4:
            return 'id_daysEcmo_cat2'
        case 5:
            return 'id_daysEcmo_cat3'
        case 6:
            return 'id_daysVent_cat1'
        case 7:
            return 'id_daysVent_cat2'
        case 8:
            return 'id_daysVent_cat3'
        case 9:
            return 'id_daysDialysis_cat1'
        case 10:
            return 'id_daysDialysis_cat2'
        case 11:
            return 'id_daysDialysis_cat3'

    }
}

function draw_output_charts(formData) {
    $.ajax({
        method: "GET",
        url: endpointRunSim,
        data: formData,
        success: function (data) {
          $('#id_output').val(JSON.stringify(data))
          ctx_med = document.getElementById('medication')
          ctx_res = document.getElementById('resources')
          ctx_consultations = document.getElementById('consultations')
          time = data['days']
          var dataMedication = []
          var dataResources = []
          var dataConsultations = [{
            'data': data['consultations'],
            'backgroundColor': '#1c73b1',
            'label': 'Consultations'
          }]
          $.each(data['medication'], function(k, v){
            dataMedication.push({})
            dataMedication[dataMedication.length-1]['label'] = k
            dataMedication[dataMedication.length-1]['data'] = v
            dataMedication[dataMedication.length-1]['fill'] = false
          })
          $.each(data['resources'], function(k, v){
            dataResources.push({})
            dataResources[dataResources.length-1]['label'] = k
            dataResources[dataResources.length-1]['data'] = v
            dataResources[dataResources.length-1]['fill'] = false
          })
          chartOutputMedication = set_chart(ctx_med, dataMedication, 'bar', 'brewer.Blues8', true, true, 'ml/mg')
          chartOutputResources = set_chart(ctx_res, dataResources, 'bar', 'tableau.ClassicBlue7', true, true, '# of remaining equipment')
          chartOutputConsultations = set_chart(ctx_consultations, dataConsultations, 'bar', '', true, false, '# of consultations')
        },
        error: function (error_data) {
          $('#id_output').val(JSON.stringify(error_data))
          console.log("error")
          console.log(error_data)
        }
    });
}

function draw_output_charts_initialized(data) {
    $('#id_output').val(JSON.stringify(data))
    ctx_med = document.getElementById('medication')
    ctx_res = document.getElementById('resources')
    ctx_consultations = document.getElementById('consultations')
    time = data['days']
    var dataMedication = []
    var dataResources = []
    var dataConsultations = [{
    'data': data['consultations'],
    'backgroundColor': ['#1c73b1'],
    'borderColor': ['#1c73b1']
    }]
    $.each(data['medication'], function(k, v){
    dataMedication.push({})
    dataMedication[dataMedication.length-1]['label'] = k
    dataMedication[dataMedication.length-1]['data'] = v
    dataMedication[dataMedication.length-1]['fill'] = false
    })
    $.each(data['resources'], function(k, v){
    dataResources.push({})
    dataResources[dataResources.length-1]['label'] = k
    dataResources[dataResources.length-1]['data'] = v
    dataResources[dataResources.length-1]['fill'] = false
    })
    chartOutputMedication = set_chart(ctx_med, dataMedication, 'bar', 'brewer.Blues8', true)
    chartOutputResources = set_chart(ctx_res, dataResources, 'bar', 'tableau.ClassicBlue7', true)
    chartOutputConsultations = set_chart(ctx_consultations, dataConsultations, 'bar', '', true, false)
}

function set_chart(ctx, data, chartType, color, showYtick, showLegend=true, ylabel=''){
var myChart = new Chart(ctx, {
  type: chartType,
  data: {
    labels: time,
    datasets: data,
  },
  options: {
    legend: {
        display: showLegend
    },
    scales: {
      yAxes: [{
          ticks: { display: showYtick },
          gridLines: {
              display: showYtick
          },
          scaleLabel:{
              display: true,
              labelString: ylabel
          }
      }],
      xAxes: [{
      scaleLabel:{
        display: true,
        labelString: 'Days'
      }}]
    },
    plugins: {
      colorschemes: {
        scheme: color
      }
    },
    elements: { points: { radius: 0  } }
  }
});
return myChart
}