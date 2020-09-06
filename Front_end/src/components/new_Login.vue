<template>



<div class="uk-grid-collapse big_box" data-uk-grid>

    

  <div class="left_box uk-width-1-2@m uk-padding-large uk-flex uk-flex-middle uk-flex-center" data-uk-height-viewport>
    <div class="uk-width-3-4@s">

		<div class="uk-text-center uk-margin-bottom">
			<a class="uk-logo uk-text-primary uk-text-bold" @click="$router.push('/home')">MealMatch</a>
		</div>
		<div class="uk-text-center uk-margin-medium-bottom">
			<h1 class="uk-h2 uk-letter-spacing-small">Sign In to MealMatch</h1>
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

      <form class="uk-text-center"  :model="loginForm">
        <div class="uk-width-1-1 uk-margin">
          <label class="uk-form-label" for="email">Email</label>
          <input v-model="loginForm.email" id="email" class="uk-input uk-form-large uk-border-pill uk-text-center" type="email" placeholder="steve@company.com">
        </div>
        <div class="uk-width-1-1 uk-margin">
          <label class="uk-form-label" for="password">Password</label>
          <input v-model="loginForm.password" id="password" class="uk-input uk-form-large uk-border-pill uk-text-center" type="password" placeholder="Min 8 characters">
        </div>
        <div class="uk-width-1-1 uk-margin uk-text-center">
          <a class="uk-text-small uk-link-muted" href="#">Forgot your password?</a>
        </div>
        <div class="uk-width-1-1 uk-text-center">
          <button class="uk-button uk-button-primary uk-button-large" @click="login">Sign In</button>
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
          <h2 class="uk-letter-spacing-small">Hello There, Join Us</h2>
        </div>
        <div class="uk-margin-top uk-margin-medium-bottom uk-text-center">
          <p>Enter your personal details and join the cooking community</p>
        </div>
        <div class="uk-width-1-1 uk-text-center">
          <button class="uk-button uk-button-primary uk-button-large" @click="signUp">Sign Up</button>
        </div>
      </div>
    </div>
  </div>


</div>


</template>

<script>
import "../assets/js/uikit.js"

export default {
    data() {
        return {
            // 
            loginForm:{
                email:'',
                password:''
            },
        
            loginFormRules: {
                //checking username
                username:[
                    {required: true, message: 'Please input username', trigger: 'blur' },
                    { min: 3, max: 5, message: 'The length of username is between 3 and 5 character', trigger: 'blur'}
                ],
                password:[
                    {required: true, message: 'Please input password', trigger: 'blur' },
                    { min: 3, max: 5, message: 'The length of password is between 3 and 5 character', trigger: 'blur'}

                ]
                //checking password
			},
			
			status:200
     

        };
    },
    methods: {
        // validate the form before submit
        login(){
               
				console.log(this.loginForm.eamil)
				console.log(this.loginForm.password)

                  

				
				this.$http.get( "login",{params:{email:this.loginForm.email,password:this.loginForm.password}}).then(res =>{
					console.log(res )
					if(res.status == 200)
					{



            this.$my_window.setItem('user_id',res.data.id)
            this.$router.push('/home');

					}
				}).catch(error =>{
					// console.log(error.response.status)
					if(error.response.status == 400)
					{
						// alert("Please check your password");
						this.$message({
							message: 'Please check your password',
							type: 'warning'
						});
					}
					if(error.response.status == 404)
					{
						this.$message.error('User not found, please check your details');
					}
					console.log("error")
				})
          
        },
        signUp(){

            this.$router.push('/SignUp');

        },
        go_to_home(){
            this.$router.push("/home")
        },
    },

    
};
</script>


<style lang="less" scoped>

    @import '../assets/css/main.css';
    @import url("https://fonts.googleapis.com/css?family=Montserrat:400,500,600&display=swap");
    @import url("https://fonts.googleapis.com/css?family=Leckerli+One&display=swap");


// .right_box{
//     transform: translate(0%,-10%);
// }

// .left_box{
//     transform: translate(0,17%);
// }

.big_box{
    transform: translate(0,-5%);
}


</style>










