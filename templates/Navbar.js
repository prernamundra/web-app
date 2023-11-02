let cross = document.getElementById('cross');
cross.style.display = 'none';

let bar = document.getElementById('bar');
let lownav = document.getElementById('lownav');
bar.addEventListener("click", function() {
    console.log('we are bar');

    lownav.innerHTML = `<div>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span><i class="fa fa-home home"></i></span> <a href = {{url_for('templates/',filename = "recruiter_dashboard.html")}} style="color: black; text-decoration: none;">&nbsp;Home</a></div>
		
    <div class="my-1">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span><i class="fa fa-briefcase briefcase"></i></span> <a href="" style="color: black; text-decoration: none;">&nbsp;Work</a></div>
    
    <div class="my-1">&nbsp;&nbsp;&nbsp;&nbsp; <span><i class="fa fa-bell bell"></i></span><a href="" style="color: black; text-decoration: none;"> &nbsp;Notification</a></div>
    
    <div class="my-1">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span><i class="fa fa-user user"></i></span> <a href="" style="color: black; text-decoration: none;"> &nbsp;&nbsp;Account</a></div>
    <div class="my-1">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span><i class="fa fa-power-off"></i></span> <a href="" style="color: black; text-decoration: none;"> &nbsp;&nbsp;Logout</a></div>
    `

    if (cross.style.display == 'none') {
        cross.style.display = 'block'
        bar.style.display = 'none';
    } else {
        cross.style.display = 'none'
        bar.style.display = 'block';
    }

});

cross.addEventListener("click", function() {
    console.log('we are bar');

    lownav.innerHTML = ``

    if (cross.style.display == 'none') {
        cross.style.display = 'block'
        bar.style.display = 'none';
    } else {
        cross.style.display = 'none'
        bar.style.display = 'block';
    }

});


let filter1 = document.getElementById("filter1");

console.log(filter1);



// select filter icon

let first = document.getElementById("first1");
let second = document.getElementById("second1");

second.style.display = "none";

console.log(first);
console.log(second);


first.addEventListener("click", function() {
    console.log('we are bar');

    filter1.innerHTML = `<div class="filter" style="cursor: pointer;">
    <div><h3 style="font-size: smaller;">Catagory</h3></div>
    <input type="text" name="" id="text" placeholder="Type here" style="font-size: smaller;">
    <hr class="hr" style="margin: 0%;">
    
    <div class="my-2"><h3 style="font-size: smaller;">Working hours</h3></div>
    <input type="text" name="" id="text" placeholder="Type here" style="font-size: smaller;">
    <hr class="hr" style="margin: 0%;">
    
    <h6 class="my-3 "  style="font-size: smaller;  ">Part Time <input type="checkbox" id="vehicle1" class="pos2" name="vehicle1" value="Bike"></h6>
    <h6 class="my-3  " style="font-size: smaller; ">Full Time<input type="checkbox" id="vehicle1" class="pos2" name="vehicle1" value="Bike"></h6>
    <h6 class="my-3  " style="font-size: smaller; ">For Men<input type="checkbox" class="pos2" id="vehicle1" name="vehicle1" value="Bike"></h6>
    <h6 class="my-3  " style="font-size: smaller; ">For Women <input type="checkbox" id="vehicle1" name="vehicle1" class="pos2" value="Bike"></h6>
    <h6 class="my-3  " style="font-size: smaller; ">Divyangsp;<input type="checkbox" class="pos2" id="vehicle1" name="vehicle1" value="Bike"></h6>

    <div class="col-12 apply" >
        <button type="submit" class="btn btn-primary apply2" >Sign in</button>
      </div>
    
</div>
`

    if (second.style.display == 'none') {
        second.style.display = 'block'
        first.style.display = 'none';
    } else {
        second.style.display = 'none'
        first.style.display = 'block';
    }

});

second.addEventListener("click", function() {
    console.log('we are bar');

    filter1.innerHTML = ``

    if (second.style.display == 'none') {
        second.style.display = 'block'
        first.style.display = 'none';
    } else {
        second.style.display = 'none'
        first.style.display = 'block';
    }

});
