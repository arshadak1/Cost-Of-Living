

const form = document.getElementById('form')
const password_match = document.getElementById('password_match')
const inputs_block = document.querySelector('.inputs-block')
const data_inputs = document.getElementById('datasForForm')
const form_msg_close = document.getElementById("form-msg-close");
const pass_msg = document.getElementById('pass_img')
const confirm_password = document.getElementById('confirm-password')
const password = document.getElementById('password')

var passwod_strength = false
const checkForm = (e) => {
    const confirm_password = document.getElementById('confirm-password')
    const password = document.getElementById('password')

    e.preventDefault(); 
    if (password.value !== confirm_password.value && !passwod_strength) {
        
        return false
    }
    else {
        
        document.getElementById('form').submit()
        return true
    }
}

confirm_password.addEventListener('keyup', (e) => {
    const confirm_password_val = document.getElementById('confirm-password').value
    const password_val = document.getElementById('password').value
    
    if (password_val !== confirm_password_val) {
        password_match.classList.remove('pass_hidden')
    
        
    }
    else {
        password_match.classList.add('pass_hidden')
    


    }
})



form_msg_close.addEventListener('click', () => {
    var alertBox = document.querySelector(".form-msg");
    alertBox.style.opacity = 0
    alertBox.style.visibility = 'hidden'

});

pass_msg.addEventListener('mouseover', () => {
    document.querySelector('.pass_msg').classList.remove('pass_msg_hidden')
})

pass_msg.addEventListener('mouseout', () => {
    document.querySelector('.pass_msg').classList.add('pass_msg_hidden')

})

password.addEventListener('keypress', (e) => {
    var decimal =  /^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[^a-zA-Z0-9])(?!.*\s).{8,35}$/;
    const pass_msg =  document.getElementById('pass_err_msg')
    if(e.value.match(decimal)){
        pass_msg.classList.add('pass_hidden')
        password.classList.remove('error-inp')
        passwod_strength = true
    }
    else {
        pass_msg.innerText = "Weak password!"
        pass_msg.classList.remove('pass_hidden')
        password.classList.add('error-inp')
    }

})
