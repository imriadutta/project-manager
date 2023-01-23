
let count = 0
let otp_gen, un
$(document).on('submit', '#post-form', function (e) {
    if (count == 0) {
        e.preventDefault();
        $.ajax({
            type: 'POST',
            url: '/sendOTP',
            data: {
                un: $('#un').val(),
                csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
            },
            success: function (data) {
                console.log(data);
                otp_gen = data
                if (otp_gen == -1) {
                    document.getElementById('otp-msg').innerHTML = 'User does not exist!'
                    count--
                }
                else {
                    $("#un").attr("disabled", "disabled")
                    document.getElementById('otp-msg').innerHTML = 'Sent an otp to your email'
                    $("#otp").css("display", "block")
                }
            }
        });
    }
    else if (count == 1) {
        e.preventDefault();
        $.ajax({
            type: 'POST',
            url: '/confirmOTP',
            data: {
                otp: $('#otp').val(),
                otp_gen: otp_gen,
                csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
            },
            success: function (data) {
                if (data == 1) {
                    $("#otp").attr("disabled", "disabled")
                    document.getElementById('otp-msg').innerHTML = 'Correct OTP!'
                    $("#new-pass").css("display", "block")
                }
                else {
                    document.getElementById('otp-msg').innerHTML = 'Wrong OTP!'
                    count--
                }
            }
        })
    }
    else if (count == 2) {
        e.preventDefault();
        $.ajax({
            type: 'POST',
            url: '/passwordChanged',
            data: {
                un: $('#un').val(),
                newpass: $('#new-pass').val(),
                csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
            },
            success: function (data) {
                if (data == 1) {
                    $("#new-pass").attr("disabled", "disabled")
                    document.getElementById('otp-msg').innerHTML = 'Password changed successfully.'
                }
                else {
                    count--
                }
            }
        })
    }
    count++
})