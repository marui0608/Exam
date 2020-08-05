$(function () {
    var check = false;
   $('#phone').blur(function () {
        var a = $(this).val();
       e = /^1[34578]\d{9}$/;
       if(!e.test(a)){
          check = false
       }else{
           check = true;
       }

   });

        $('#code').click(function () {
            if(check){


            $.ajax({
                type: 'post',
                url: '/author/author_code/',
                data:{
                    csrfmiddlewaretoken:$('[name="csrfmiddlewaretoken"]').val(),
                    mobile: $('#phone').val()
                },
                success:function (ad) {
                    alert(ad.data)
                },

            })
         }else(alert('请输入正确的手机号')) });


});