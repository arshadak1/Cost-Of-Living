const ham_menu = document.querySelector('.menu-5');
const menu = document.querySelector('.menu');
const container = document.querySelector('.container');
// const footer = document.querySelector('.footer');


let width, height;
window.onresize = window.onload = function () {
  width = this.innerWidth;
  if (width > 1000) {
    menu.classList.remove('hidden')
    container.classList.remove('hidden')
    // footer.classList.remove('hidden')
  }
  else {
    menu.classList.add('hidden')
    container.classList.add('hidden')
    // footer.classList.add('hidden')
  }
}

let curr_path = window.location.pathname
if(curr_path == '/dashboard'){
  const curr_menu = document.querySelector('#dashboard-menu')
  curr_menu.classList.add('menu-selected')

}

else if(curr_path == '/review'){
  const curr_menu = document.querySelector('#reviews-menu')
  curr_menu.classList.add('menu-selected')

}

else if(curr_path == '/dashboard/profile'){
  const curr_menu = document.querySelector('#profile-menu')
  curr_menu.classList.add('menu-selected')

}

else if(curr_path == '/dashboard/graphs'){
  const curr_menu = document.querySelector('#graphs-menu')
  curr_menu.classList.add('menu-selected')

}

else if((/\/dashboard\/data.*/i).test(curr_path)){
  const curr_menu = document.querySelector('#data-menu')
  curr_menu.classList.add('menu-selected')

}



ham_menu.addEventListener('click', (e) => {
  if (ham_menu.classList.contains('active')) {
    ham_menu.classList.toggle('back')
  } else {
    ham_menu.classList.toggle('active')
  }

  menu.classList.toggle('hidden')
  container.classList.toggle('hidden')
  footer.classList.toggle('hidden')

})

