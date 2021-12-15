$(window).scroll(function() {
    

    var height = $('img#id_headerImg').height();
    height *= 0.9;
    $('nav').toggleClass('scrolled', $(this).scrollTop()>height);
    if ($(this).scrollTop()>height) {
        $('.navlink-top').addClass('dark');
        $('.navbar-top').removeClass('navbar-dark');
        $('.navbar-top').addClass('navbar-light');
        $('.second-nav').addClass('shadow');
        $('#id_saveExport').show()
        $('id_saveForm').show()
        $('#id_simFrom').show()
    }
    else {
        $('.navbar-top').removeClass('navbar-light');
        $('.navbar-top').addClass('navbar-dark');
        $('.navlink-top').removeClass('dark');
        $('.second-nav').removeClass('shadow');
        $('#id_saveExport').hide()
        $('id_saveForm').hide()
        $('#id_simFrom').hide()
    }
})

$('.navbar-top').removeClass('navbar-light');
$('.navbar-top').removeClass('bg-white');
$('.navbar-top').addClass('bg-primary');
$('.navbar-top').addClass('navbar-dark');
$('.navlink-top').removeClass('dark');
$('.second-nav').removeClass('shadow');
$('#id_saveExport').hide()
$('#id_saveForm').hide()