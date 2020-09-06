<template>
<div>
<nav class="uk-navbar-container uk-letter-spacing-small">
  <div class="uk-container">
    <div class="uk-position-z-index" data-uk-navbar>
      <div class="uk-navbar-left">
        <a class="uk-navbar-item uk-logo" @click="go_to_home">MealMatch</a>

      </div>
      <div class="uk-navbar-right">
        <div>

        </div>
        <ul class="uk-navbar-nav uk-visible@m">
          <li ><a @click="$router.push('/login')">Sign In</a></li>
          <li ><a @click="create_recipe">Create Recipe</a></li>
        </ul>
        <div class="uk-navbar-item">
          <div><a class="uk-button uk-button-primary" @click="$router.push('/SignUp')">Sign Up</a></div>
        </div>          
        <a class="uk-navbar-toggle uk-hidden@m" href="#offcanvas" data-uk-toggle><span
          data-uk-navbar-toggle-icon></span></a>
      </div>
    </div>
  </div>
</nav>


<div class="uk-container">
  <div class="uk-border-rounded-large uk-background-top-center uk-background-cover 
    uk-background-norepeat uk-light uk-inline uk-overflow-hidden uk-width-1-1" 
    style="background-image: url(https://www.diabetes.co.uk/wp-content/uploads/2019/01/What-to-eat-on-a-ketogenic-diet.png);">
    <div class="uk-position-cover uk-header-overlay"></div>
    <div class="uk-position-relative" data-uk-grid>
      <div class="uk-width-1-2@m uk-flex uk-flex-middle">
        <div class="uk-padding-large uk-padding-remove-right">
          <h1 class="uk-heading-small uk-margin-remove-top">Hello <a class='uk-text-bold uk-text-warning' style="color:#EB4A36; ">{{user.username}}</a></h1>
          <p class="uk-text-secondary"></p>

        </div>
      </div>
      <div class="uk-width-expand@m">
      </div>
    </div>
  </div>
</div>

<br>
<div class="uk-flex uk-flex-center uk-background-muted">
    <div>
        <h1 >Your details</h1>
    </div>
</div>


           
<div  class="uk-container uk-container-small">
    <div v-for="(value,name,index) in user" class="uk-grid-small uk-margin-medium-top" data-uk-grid>
        <div class="uk-width-auto">
        <a href="#" class="uk-step-icon" data-uk-icon="icon:  happy; ratio: 0.8" 
            data-uk-toggle="target: #step-1; cls: uk-step-active"></a>
        </div>
            <div class="uk-width-expand">
            <h5 class="uk-step-title uk-text-500 uk-text-uppercase uk-text-primary" data-uk-leader="fill:—">{{index+1}}. {{name}}</h5>

            <form>
                <div class='uk-margin'>    
                    <div class="uk-inline">
                        <input class="uk-input uk-border-pill uk-form-width-large" type="text" v-model = "user[name]"  >
                    </div>
                </div>

            </form>
        </div>
    </div>
    <div class="uk-flex uk-flex-center">
        <a class="uk-button uk-button-primary uk-button-large uk-width-1-4" @click="saveChanges">Save</a>
    </div>
</div>
<br>
<div class="uk-flex uk-flex-center uk-background-muted">
    <div>
        <h1 >Your Recipes</h1>
    </div>
</div>

    


<br>
  <div class="uk-container uk-container-small">

            <div  class="uk-child-width-1-2 uk-child-width-1-3@s" data-uk-grid>
                <div v-for="object in recipes_list">
                <div v-if="object.id>=0"  class="uk-card">
                    <div class="uk-card-media-top uk-inline uk-light">
                    <img class="uk-border-rounded-medium" :src="getImgUrl(object.img)" alt="Course Title" style="width:250px; height:150px;">
                    <div class="uk-position-cover uk-card-overlay uk-border-rounded-medium"></div>
                    <div class="uk-position-xsmall uk-position-top-right">
                        <a @click="remove_recipe(object)" class="uk-icon-button uk-like uk-position-z-index uk-position-relative"
                        data-uk-icon="close"></a>
                    </div>
                    </div>
                    <div>
                    <h3 class="uk-card-title uk-text-500 uk-margin-small-bottom uk-margin-top">{{object.name}}</h3>
                    <div class="uk-text-xsmall uk-text-muted" data-uk-grid>
                        <div class="uk-width-auto uk-flex uk-flex-middle">
                        <span class="uk-rating-filled" data-uk-icon="icon: star; ratio: 0.7"></span>
                        </div>
                        <div class="uk-width-expand uk-text-right">{{object.author}}</div>
                    </div>
                    </div>
                    <a @click="add_recipe_id(object.id)" class="uk-position-cover"></a>
                </div>
                </div>
            </div>
        
    </div>
    <br>




<div class="uk-flex uk-flex-center uk-background-muted">
    <div>
        <h1 >Matched users</h1>
    </div>
</div>
<br>
<div class="uk-container uk-container-small">
<div class="uk-child-width-1-2@s uk-grid-match" uk-grid>

    <div v-for="user in match_users">
        <div class="uk-card uk-card-default uk-card-hover uk-card-body" @click="show_recipe_users(user.user_id)">
            <h2 >{{user.username}}</h2>
            <p>Email: {{user.email}}</p>
            <!-- <p>Favorite_ingredients: {{user.favourite_ingredients}}</p> -->
            <a>Recipes created: </a>
            <el-collapse-transition>
                <div v-if="show == user.user_id">
                    <ul v-for="recipe in mathched_recipe_list">
                        <li><a class="transition-box" @click="add_recipe_id(recipe.id)">{{recipe.name}}</a></li>
                    </ul>
                </div>
            </el-collapse-transition>
        </div>
    </div>


</div>
</div>
<br>










<footer class="uk-section uk-section-default uk-background-muted">
	<div class="uk-container uk-text-secondary uk-text-500">
		<div class="uk-child-width-1-2@s" data-uk-grid>
			<div>
				<a href="#" class="uk-logo">MealMatch</a>
			</div>
			<div class="uk-flex uk-flex-middle uk-flex-right@s">
				<div data-uk-grid class="uk-child-width-auto uk-grid-small">
					<div>
						<a href="https://www.facebook.com/" data-uk-icon="icon: facebook; ratio: 0.8" class="uk-icon-button facebook" target="_blank"></a>
					</div>
					<div>
						<a href="https://www.instagram.com/" data-uk-icon="icon: instagram; ratio: 0.8" class="uk-icon-button instagram" target="_blank"></a>
					</div>
					<div>
						<a href="mailto:info@blacompany.com" data-uk-icon="icon: twitter; ratio: 0.8" class="uk-icon-button twitter" target="_blank"></a>
					</div>
				</div>
			</div>
		</div>
		
			
	

	</div>
</footer>







</div>






</template>




<<script>
export default {
    data() {
        return {
            user:{
                username:'Steve',
                email:"729114838@qq.com",
                password:'1234',
            },
            recipes_list:[
                {
                    name:"tomato beef",
                    img:"burger.png",
                    author:"steve",
                    id:4
                },
                {
                    name:"tomato beef",
                    img:"veg.png",
                    author:"steve",
                    id:5
                }
                
            ],
            mathched_recipe_list:[              
                {
                    name:"tomato beef",
                    img:"burger.png",
                    author:"steve",
                    id:4
                },
                {
                    name:"tomato beef",
                    img:"veg.png",
                    author:"steve",
                    id:5
                }
            ],
            show:-1,
            user_id: -1,
            match_users:[
                {
                    username:"steve",
                    email:"abc@qq.com",
                    favourite_ingredients:"apple, pepper",
                    user_id: 1,
                 
                },
                {
                    username:"eamon",
                    email:"eamon@qq.com",
                    favourite_ingredients:"apple, pepper, cabbage",
                    user_id:2
                },
                {
                    username:"ISa",
                    email:"Isa@qq.com",
                    favourite_ingredients:"apple, pepper, cabbage,onion",
                    user_id:3
                }

            ]
        }
        // ,
  
    },  
        mounted() {
            this.user_id= this.$my_window.getItem('user_id')
            this.init(this.user_id)
        },  
    methods:{

        show_recipe_users(input_id){
            if(this.show == input_id)
            {
                this.show = -1
            }else{
                this.show= input_id
            }
            console.log("shoowwwwww" + this.show + input_id)
            

            this.$http.get("get_user_recipes",{params:{id:input_id}}).then( res => {
                console.log(res.data)
                this.mathched_recipe_list = res.data
            }).catch(err => {
                console.log(err.response)
                this.$message({
                    message: 'This user has not creat any recipe',
                    type: 'warning'
                });
                this.mathched_recipe_list = [];
            })


        },
        create_recipe(){
          if(this.user_id == null || this.user_id == -1)
          {
            this.$message({
							message: 'Please sigin or create account',
							type: 'warning'
						});
          }else
          {
            this.$router.push("/create_recipe");
          }
        },
        saveChanges(){
            const params = new URLSearchParams();
            params.append('username',this.user.username)
            params.append('email',this.user.email)
            params.append('password',this.user.password)
            params.append('id',this.user_id)

            this.$http.post("save_changes",params).then(
                res => {
                    this.$message({
                        message: 'Changes saved',
                        type: 'success'
                    })
                }
            )  
        },
        init(input_id){
            this.$http.get("get_user_info",{params:{id:input_id}}).then( res => {
                console.log(res.data)
                this.user = res.data
            })
            this.$http.get("get_user_recipes",{params:{id:input_id}}).then( res => {
                console.log(res.data)
                this.recipes_list = res.data
            }).catch(err => {
                console.log(err.response)
                this.recipes_list = [];
            })
            this.$http.get("recommend_friend", {params:{id:input_id}}).then(res => {
                this.match_users = res.data
            })
        },
        add_recipe_id: function(id){
            
            this.$my_window.setItem('recipe_id',id)
            this.$router.push('/recipe');

        },
        go_to_home(){
            this.$router.push("/home")
        },
        getImgUrl(pic) {
            if(pic != "")
            {
                return require('../assets/img/'+pic)
            }
            return require('../assets/img/mango.png')
        },
        remove_recipe(recipe)
        {
            this.$confirm('Are you sure want to delete this recipe','Warning',{
                
                cancelButtonText: 'Cancel',
                confirmButtonText: 'Confirm',
                type: 'warning'
            }).then(() => {


                this.$http.delete("recipe/delete_recipe",{params:{id:recipe.id}}).then(res => {
                
                })
                this.recipes_list[this.recipes_list.indexOf(recipe)].id = -1
                this.$http.get("get_user_recipes",{params:{id:this.user_id}}).then( res => {
                    console.log(res.data)
                    this.recipes_list = res.data
                }).catch(err => {
                    console.log(err.response)
                    this.recipes_list = [];
                })

                this.$message({
                    message: 'Recipe is removed',
                    type: 'success'
                });
            })  

        }
    


    }
}
</script>>

