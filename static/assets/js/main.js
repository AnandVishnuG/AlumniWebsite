/**
* Template Name: Tempo
* Updated: Mar 10 2023 with Bootstrap v5.2.3
* Template URL: https://bootstrapmade.com/tempo-free-onepage-bootstrap-theme/
* Author: BootstrapMade.com
* License: https://bootstrapmade.com/license/
*/
(function() {
  "use strict";

  /**
   * Easy selector helper function
   */
  const select = (el, all = false) => {
    el = el.trim()
    if (all) {
      return [...document.querySelectorAll(el)]
    } else {
      return document.querySelector(el)
    }
  }

  /**
   * Easy event listener function
   */
  const on = (type, el, listener, all = false) => {
    let selectEl = select(el, all)
    if (selectEl) {
      if (all) {
        selectEl.forEach(e => e.addEventListener(type, listener))
      } else {
        selectEl.addEventListener(type, listener)
      }
    }
  }

  /**
   * Easy on scroll event listener 
   */
  const onscroll = (el, listener) => {
    el.addEventListener('scroll', listener)
  }

  /**
   * Navbar links active state on scroll
   */
  let navbarlinks = select('#navbar .scrollto', true)
  const navbarlinksActive = () => {
    let position = window.scrollY + 200
    navbarlinks.forEach(navbarlink => {
      if (!navbarlink.hash) return
      let section = select(navbarlink.hash)
      if (!section) return
      if (position >= section.offsetTop && position <= (section.offsetTop + section.offsetHeight)) {
        navbarlink.classList.add('active')
      } else {
        navbarlink.classList.remove('active')
      }
    })
  }
  window.addEventListener('load', navbarlinksActive)
  onscroll(document, navbarlinksActive)

  /**
   * Scrolls to an element with header offset
   */
  const scrollto = (el) => {
    let header = select('#header')
    let offset = header.offsetHeight

    if (!header.classList.contains('header-scrolled')) {
      offset -= 16
    }

    let elementPos = select(el).offsetTop
    window.scrollTo({
      top: elementPos - offset,
      behavior: 'smooth'
    })
  }

  /**
   * Toggle .header-scrolled class to #header when page is scrolled
   */
  let selectHeader = select('#header')
  if (selectHeader) {
    const headerScrolled = () => {
      if (window.scrollY > 100) {
        selectHeader.classList.add('header-scrolled')
      } else {
        selectHeader.classList.remove('header-scrolled')
      }
    }
    window.addEventListener('load', headerScrolled)
    onscroll(document, headerScrolled)
  }

  /**
   * Back to top button
   */
  let backtotop = select('.back-to-top')
  if (backtotop) {
    const toggleBacktotop = () => {
      if (window.scrollY > 100) {
        backtotop.classList.add('active')
      } else {
        backtotop.classList.remove('active')
      }
    }
    window.addEventListener('load', toggleBacktotop)
    onscroll(document, toggleBacktotop)
  }

  /**
   * Mobile nav toggle
   */
  on('click', '.mobile-nav-toggle', function(e) {
    select('#navbar').classList.toggle('navbar-mobile')
    this.classList.toggle('bi-list')
    this.classList.toggle('bi-x')
  })

  /**
   * Mobile nav dropdowns activate
   */
  on('click', '.navbar .dropdown > a', function(e) {
    if (select('#navbar').classList.contains('navbar-mobile')) {
      e.preventDefault()
      this.nextElementSibling.classList.toggle('dropdown-active')
    }
  }, true)

  /**
   * Scrool with ofset on links with a class name .scrollto
   */
  on('click', '.scrollto', function(e) {
    if (select(this.hash)) {
      e.preventDefault()

      let navbar = select('#navbar')
      if (navbar.classList.contains('navbar-mobile')) {
        navbar.classList.remove('navbar-mobile')
        let navbarToggle = select('.mobile-nav-toggle')
        navbarToggle.classList.toggle('bi-list')
        navbarToggle.classList.toggle('bi-x')
      }
      scrollto(this.hash)
    }
  }, true)

  /**
   * Porfolio isotope and filter
   */
  window.addEventListener('load', () => {
    let portfolioContainer = select('.portfolio-container');
    if (portfolioContainer) {
      let portfolioIsotope = new Isotope(portfolioContainer, {
        itemSelector: '.portfolio-item',
        layoutMode: 'fitRows'
      });

      let portfolioFilters = select('#portfolio-flters li', true);

      on('click', '#portfolio-flters li', function(e) {
        e.preventDefault();
        portfolioFilters.forEach(function(el) {
          el.classList.remove('filter-active');
        });
        this.classList.add('filter-active');

        portfolioIsotope.arrange({
          filter: this.getAttribute('data-filter')
        });

      }, true);
    }

  });
  /** Post filter and isotope */
window.addEventListener('load', () => {

  let postContainer = select('.post-container');
  if (postContainer) {
    let postIsotope = new Isotope(postContainer, {
      itemSelector: '.post-item',
      layoutMode: 'vertical',
    });

    let postFilters = select('#post-filters li', true);

    on('click', '#post-filters li', function(e) {
      e.preventDefault();
      postFilters.forEach(function(el) {
        el.classList.remove('filter-active');
      });
      this.classList.add('filter-active');

      postIsotope.arrange({
        filter: this.getAttribute('data-filter')
      });
    }, true);
  }
});

  
  /**
   * Initiate portfolio lightbox 
   */
  const portfolioLightbox = GLightbox({
    selector: '.portfolio-lightbox'
  });

  /**
   * Portfolio details slider
   */
  new Swiper('.portfolio-details-slider', {
    speed: 400,
    loop: true,
    autoplay: {
      delay: 5000,
      disableOnInteraction: false
    },
    pagination: {
      el: '.swiper-pagination',
      type: 'bullets',
      clickable: true
    }
  });

  /**
   * Scroll with ofset on page load with hash links in the url
   */
  window.addEventListener('load', () => {
    if (window.location.hash) {
      if (select(window.location.hash)) {
        scrollto(window.location.hash)
      }
    }
  });

})()

document.addEventListener('DOMContentLoaded', function() {

  /**
   * Update choices when post is being created
   */
  
  let pollForm = document.querySelectorAll(".poll-form")
  let container = document.querySelector("#form-container")
  let choiceContainer = document.querySelector("#choice_container")
  let addButton = document.querySelector("#add-form")
  let delButton = document.querySelector("#delete-form")

  let totalForms = document.querySelector("#id_form-TOTAL_FORMS")
  let formNum = pollForm.length-1 
  if (addButton){
  addButton.addEventListener('click', addForm)
  delButton.addEventListener('click', delForm)
}
  function addForm(e) {
    e.preventDefault()

    let newForm = pollForm[0].cloneNode(true) //Clone the poll form
    let formRegex = RegExp(`form-(\\d){1}-`,'g') //Regex to find all instances of the form number
    let formRegex2 = RegExp(`Choice\\s(\\d){1}`,'g')
    formNum++ //Increment the form number
    newForm.innerHTML = newForm.innerHTML.replace(formRegex, `form-${formNum}-`) //Update the new form to have the correct form number
    newForm.innerHTML = newForm.innerHTML.replace(formRegex2, `Choice ${formNum+1}`)
    // newForm.placeholder = `Choice ${formNum + 1}`
    choiceContainer.appendChild(newForm) //Insert the new form at the end of the list of forms
    
    totalForms.setAttribute('value', `${formNum+1}`) //Increment the number of total forms in the management form

  }

  function delForm(e) {
    e.preventDefault()

    // Get the form to be deleted
    let pollForm = document.querySelectorAll(".poll-form")
    let formNum = pollForm.length-1 
    let formToDelete = pollForm[formNum]

    // Check if the form exists
    if (formToDelete) {
      // Delete the form
      formToDelete.remove()

      // Decrement the number of total forms
      let totalForms = document.querySelector("#id_form-TOTAL_FORMS")
      totalForms.setAttribute('value', `${totalForms.value - 1}`)
      }
  }

});
// Step javascript

function showElement(elementId) {
  var questionContainer = document.getElementById('question_container');
  var pdateContainer = document.getElementById('pdate_container');
  var choiceContainer = document.getElementById('choice_container');
  var beforePdateContainer = document.getElementById('step_1')
  let btnContainer = document.querySelector("#btn-form")
  let btnSubmit = document.querySelector("#btn-submit")
  
  // Hide all containers
  questionContainer.style.display = 'none';
  pdateContainer.style.display = 'none';
  choiceContainer.style.display = 'none';
  btnContainer.style.display = 'none';
  btnSubmit.style.display = 'none';
  // Show the appropriate container
  switch (elementId) {
    case 'question_container':
      questionContainer.style.display = 'block';
      break;
    case 'pdate_container':
      pdateContainer.style.display = 'block';
      btnSubmit.style.display = 'block';
      
      break;
    case 'choice_container':
      choiceContainer.style.display = 'block';
      btnContainer.style.display = 'block';
      break;
  }
}
// Setting centering for Publish_date
document.addEventListener('DOMContentLoaded', function() {

// Center stepper 2 pd_date
// get the parent and child elements
var parent = document.getElementById('pdate_container');
if (parent){
var child = parent.firstElementChild;

// set the left property of the child element
child.style.left = '20%';
}
});