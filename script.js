$('a').on('click', function(e) {
    let clickedDeviceName = e.target.innerText;
    let macAddress = e.target.id;

    $.ajax({
        url: '/process_device_data',
        method: 'post',
        dataType: 'html',
        data: {
            'clicked_device_name': clickedDeviceName,
            'mac_device_address': macAddress
        },
        success: function(data){
            alert(JSON.parse(data).operation_result_text);
        },
    });
})

(function(){
    var burger = document.querySelector('.burger-container'),
        header = document.querySelector('.header');
    
    burger.onclick = function() {
        header.classList.toggle('menu-opened');
    }
}());