/*!
 * toast.js v0.1.0
 * (c) 2022 brainelectronics
 * Released under the MIT License
 */
function createToast(t,e,i,s){var n=document.createElement("div");n.classList.add("alert"),t&&n.classList.add(t),n.style.position="relative",n.style.width="100%",n.style.maxWidth="300px",n.style.minWidth="280px",n.style.borderRadius="5px",n.style.padding="15px",n.innerHTML="<strong>"+e+"</strong> "+i,document.getElementById("alert_container").appendChild(n),setTimeout(function(){n.style.opacity=1,n.style.visibility="visible"},1),s>0?setTimeout(function(){n.style.opacity=0,n.style.visibility="hidden",setTimeout(function(){n.remove()},350)},s):null==s&&setTimeout(function(){n.style.opacity=0,n.style.visibility="hidden",setTimeout(function(){n.remove()},350)},3e3)}