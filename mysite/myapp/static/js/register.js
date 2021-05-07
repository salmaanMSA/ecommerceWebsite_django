const first_nameField=document.querySelector('#first_nameField');
const first_nameFeedBackArea=document.querySelector('.first_nameFeedBackArea');
const firstnameSuccessOutput=document.querySelector(".firstnameSuccessOutput");

const last_nameField=document.querySelector('#last_nameField');
const last_nameFeedBackArea=document.querySelector('.last_nameFeedBackArea');
const lastnameSuccessOutput=document.querySelector(".lastnameSuccessOutput");

const emailField=document.querySelector('#emailField');
const emailFeedBackArea=document.querySelector('.emailFeedBackArea');
const emailSuccessOutput=document.querySelector(".emailSuccessOutput");

const mobile_noField=document.querySelector('#mobile_noField');
const mobile_noFeedBackArea=document.querySelector('.mobile_noFeedBackArea');
const mobile_noSuccessOutput=document.querySelector(".mobile_noSuccessOutput");

const passwordField=document.querySelector('#passwordField');
const showPasswordToggle=document.querySelector(".showPasswordToggle");

const submitBtn = document.querySelector(".submit-btn");



const handleToggleInput=(e)=>{

    if(showPasswordToggle.textContent ==="SHOW") {
        showPasswordToggle.textContent = "HIDE";

        passwordField.setAttribute("type","text");

    } else {
        showPasswordToggle.textContent = "SHOW";
        passwordField.setAttribute("type","password");
    }

}

showPasswordToggle.addEventListener('click', handleToggleInput)


emailField.addEventListener('keyup', (e) => {
    const emailVal = e.target.value;

    emailSuccessOutput.style.display = "block";

    //emailSuccessOutput.textContent=`Checking  ${emailVal}`;

    emailField.classList.remove("is-invalid");
    emailFeedBackArea.style.display = "none";

    if(emailVal.length > 0 ) {
        fetch("/validate-email",{
            body:JSON.stringify({ email : emailVal }),
            method: "POST",
        })
            .then((res) => res.json())
            .then((data) => {
                console.log("data",data);
                emailSuccessOutput.style.display = "none";
                if (data.email_error) {
                    submitBtn.disabled = true;
                    emailField.classList.add("is-invalid");
                    emailFeedBackArea.style.display = "block";
                    emailFeedBackArea.innerHTML= `<p>${data.email_error}</p>`
                }else {
                submitBtn.removeAttribute("disabled");
                }
            });
    }


});

//first_name

first_nameField.addEventListener('keyup', (e) => {
    console.log('777777',777777);
    const first_nameVal = e.target.value;

    //first_nameSuccessOutput.style.display = "block";

    firstnameSuccessOutput.textContent=`Checking  ${first_nameVal}`;

    first_nameField.classList.remove("is-invalid");
    first_nameFeedBackArea.style.display = "none";

    if(first_nameVal.length > 0 ) {
        fetch("/validate-first_name",{
            body:JSON.stringify({ first_name : first_nameVal }),
            method: "POST",
        })
            .then((res) => res.json())
            .then((data) => {
                console.log("data",data);
                firstnameSuccessOutput.style.display = "none";
                if (data.first_name_error) {
                    first_nameField.classList.add("is-invalid");
                    first_nameFeedBackArea.style.display = "block";
                    first_nameFeedBackArea.innerHTML= `<p>${data.first_name_error}</p>`
                    submitBtn.disabled = true;

                }else{
                submitBtn.removeAttribute("disabled");
                }
            });
    }


});

//last_name

last_nameField.addEventListener('keyup', (e) => {
    console.log('777777',777777);
    const last_nameVal = e.target.value;

    //lastnameSuccessOutput.style.display = "block";

    lastnameSuccessOutput.textContent=`Checking  ${last_nameVal}`;

    last_nameField.classList.remove("is-invalid");
    last_nameFeedBackArea.style.display = "none";

    if(last_nameVal.length > 0 ) {
        fetch("/validate-last_name",{
            body:JSON.stringify({ last_name : last_nameVal }),
            method: "POST",
        })
            .then((res) => res.json())
            .then((data) => {
                console.log("data",data);
                lastnameSuccessOutput.style.display = "none";
                if (data.last_name_error) {
                    last_nameField.classList.add("is-invalid");
                    last_nameFeedBackArea.style.display = "block";
                    last_nameFeedBackArea.innerHTML= `<p>${data.last_name_error}</p>`
                    submitBtn.disabled = true;

                }else{
                submitBtn.removeAttribute("disabled");
                }
            });
    }

});

//mobile_no

mobile_noField.addEventListener('keyup', (e) => {
    console.log('777777',777777);
    const mobile_noVal = e.target.value;

    //mobile_noSuccessOutput.style.display = "block";

    mobile_noSuccessOutput.textContent=`Checking  ${mobile_noVal}`;

    mobile_noField.classList.remove("is-invalid");
    mobile_noFeedBackArea.style.display = "none";

    if(mobile_noVal.length > 0 ) {
        fetch("/validate-mobile_no",{
            body:JSON.stringify({ mobile_no : mobile_noVal }),
            method: "POST",
        })
            .then((res) => res.json())
            .then((data) => {
                console.log("data",data);
                mobile_noSuccessOutput.style.display = "none";
                if (data.mobile_no_error) {
                    mobile_noField.classList.add("is-invalid");
                    mobile_noFeedBackArea.style.display = "block";
                    mobile_noFeedBackArea.innerHTML= `<p>${data.mobile_no_error}</p>`
                    submitBtn.disabled = true;

                }else{
                submitBtn.removeAttribute("disabled");
                }
            });
    }

});
