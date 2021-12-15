$(document).ready(function() {
   $('#inputs input').change(function() {
        var tend = $("tend").val();
        var narrivals = [$("lowRiskArrivals").val(), $("medRiskArrivals").val(), $("highRiskArrivals").val()];
        var totalmean = [$("lowRiskLos").val(), $("medRiskLos").val(), $("highRiskLos").val()];
        var ventmean = [$("lowRiskVentLos").val(), $("medRiskVentLos").val(), $("highRiskVentLos").val()];
        var icu = {
            "mortrate": [$("mortrate_iculr").val(), $("mortrate_icumr").val(), $("mortrate_icuhr").val()],
            "nmri": $("#icumri").val(),
            "nct": $("#icuct").val(),
            "nxray": $("#icuxray").val()
        }
        var ward = {
            "mortrate": [$("mortrate_wardlr").val(), $("mortrate_wardmr").val(), $("mortrate_wardhr").val()],
            "nmri": $("#wardmri").val(),
            "nct": $("#wardct").val(),
            "nxray": $("#wardxray").val()
        }
        var ward = {
            "nmri": $("#ermri").val(),
            "nct": $("#erct").val(),
            "nxray": $("#erxray").val()
        }


   });
});

