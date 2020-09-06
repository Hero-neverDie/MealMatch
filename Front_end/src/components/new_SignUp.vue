<template>



<div class="uk-grid-collapse big_box" data-uk-grid>

    
  <div class="left_box uk-width-1-2@m uk-padding-large uk-flex uk-flex-middle uk-flex-center" data-uk-height-viewport>
    <div class="uk-width-3-4@s">
      <div class="uk-text-center uk-margin-bottom">
        <a class="uk-logo uk-text-primary uk-text-bold" @click="$router.push('/home')">MealMatch</a>
      </div>
      <div class="uk-text-center uk-margin-medium-bottom">
        <h1 class="uk-h2 uk-letter-spacing-small">Registration</h1>
      </div>
      <div data-uk-grid class="uk-child-width-auto uk-grid-small uk-flex uk-flex-center uk-margin">
        <div>
          
          <img src="../assets/img/veg.png" alt="veg" width="60">
        </div>
        <div>
          <img src="../assets/img/mango.png" alt="mango" width="60">
        </div>
        <div>
          <img src="../assets/img/carrot.png" alt="carrot" width="60">
        </div>
      </div>    


      <form class="uk-text-center"  :model="SignUpForm">
        <div class="uk-width-1-1 uk-margin">
          <label class="uk-form-label" for="username">username</label>
          <input v-model="SignUpForm.username" id="username" class="uk-input uk-form-large uk-border-pill uk-text-center" type="username" placeholder="Username">
        </div>
        <div class="uk-width-1-1 uk-margin">
          <label class="uk-form-label" for="email">Email</label>
          <input v-model="SignUpForm.email" id="email" class="uk-input uk-form-large uk-border-pill uk-text-center" type="email" placeholder="steve@company.com">
        </div>
        <div class="uk-width-1-1 uk-margin">
          <label class="uk-form-label" for="password">Password</label>
          <input v-model="SignUpForm.password" id="password" class="uk-input uk-form-large uk-border-pill uk-text-center" type="password" placeholder="Min 8 characters">
        </div>
        <div class="uk-width-1-1 uk-text-center">
          <button class="uk-button uk-button-primary uk-button-large" @click="SignUp">Sign Up</button>
        </div>
      </form>
    </div>
  </div>
  <div class="right_box uk-width-1-2@m uk-padding-large uk-flex uk-flex-middle uk-flex-center uk-light" data-uk-height-viewport>
    <div class="uk-background-cover uk-background-norepeat uk-background-blend-overlay uk-background-overlay 
      uk-border-rounded-large uk-width-1-1 uk-height-xlarge uk-flex uk-flex-middle uk-flex-center" 
      style="background-image: url(https://www.diabetes.co.uk/wp-content/uploads/2019/01/What-to-eat-on-a-ketogenic-diet.png);">
      <div class="uk-padding-large">
        <div class="uk-text-center">
          <h2 class="uk-letter-spacing-small">Welcome Back</h2>
        </div>
        <div class="uk-margin-top uk-margin-medium-bottom uk-text-center">
          <p>Already signed up, enter your details and start exploring our wide range of recipes</p>
        </div>
        <div class="uk-width-1-1 uk-text-center">
          <button class="uk-button uk-button-primary uk-button-large" @click="loginPage">Sign in</button>
        </div>
      </div>
    </div>
  </div>
</div>


</template>

<script>
export default {
    data() {
        return {
            // 
            SignUpForm:{
				email:'',
				username:'',
                password:''
            },
        
           
			
			status:200
     

        };
    },
    methods: {
        // validate the form before submit
        SignUp(){
               
				// console.log(this.SignUpForm)
				// console.log(this.status +"1")
			  
				const params = new URLSearchParams();
				params.append('username',this.SignUpForm.username)
				params.append('email',this.SignUpForm.email)
				params.append('password',this.SignUpForm.password)
			      
			   
        this.$http.post("signup",params).then(
				  res =>{
						console.log("/"+res.status+"/");

						if(res.status == 201)
						{
							this.$message({
								message: 'SignUp successful!',
								type: 'success'
              });
              window.sessionStorage.setItem('user_id',res.data.id)
							this.$router.push('/home');
						}else if(res.status == 200)
            {
              this.$message({
								message: 'email is already used',
								type: 'warning'
              });
            }  
                      
				  })
				  .catch(error =>{
					  console.log("/"+error.response.status+"/")
				  });

				

					
					 
		
          
        },
        loginPage(){

            this.$router.push('/');

        }
    },

    
};
</script>


<style lang="less" scoped>

    @import '../assets/css/main.css';
    @import url("https://fonts.googleapis.com/css?family=Montserrat:400,500,600&display=swap");
    @import url("https://fonts.googleapis.com/css?family=Leckerli+One&display=swap");


// .right_box{
//     transform: translate(90%,-80%);
// }

// .left_box{
//     transform: translate(0,17%);
// }

.big_box{
    transform: translate(0,-8%);
}


</style>










