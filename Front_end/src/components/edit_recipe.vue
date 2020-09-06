<template>
<div>
<nav class="uk-navbar-container uk-letter-spacing-small">
  <div class="uk-container">
    <div class="uk-position-z-index" data-uk-navbar>
      <div class="uk-navbar-left">
        <a class="uk-navbar-item uk-logo" @click="go_to_home">MealMatch</a>
      </div>
      <div class="uk-navbar-right">
        <ul class="uk-navbar-nav uk-visible@m">
            <li><a uk-icon="user"  @click="go_to_profile"></a><li>
             
            <li ><a @click="goto_login">Sign In</a></li>
            <li ><a @click="create_recipe">Create Recipe</a></li> 

        </ul>
        <div class="uk-navbar-item">
            <div>
                <a class="uk-button uk-button-primary" @click="goto_signup">Sign Up</a></div>
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
          <h1 class="uk-heading-small uk-margin-remove-top">Hello <a class='uk-text-bold uk-text-warning' style="color:#EB4A36; ">{{recipe.author}}</a></h1>
          <p class="uk-text-secondary">With MealMatch, you can create your own recipes in the easiest way!</p>

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
        <h1 >Edit your Recipe</h1>
    </div>
</div>
<div class="uk-section uk-section-default">


    <div class="uk-container uk-container-small">
        <div class="uk-grid-large" data-uk-grid>
            <div class="uk-width-expand@m">
                <h3>1 - Description:</h3>
                <form>
                    <div class='uk-margin'>    
                        
                        <input class="uk-input uk-border-pill uk-form-width-large"   v-model="recipe.description" placeholder="Tell us more about yout recipe " >
                        
                    </div>
                </form>

            </div>
            <div class="uk-width-1-3@m">
                <h3>2 - Name of recipe:</h3>
                <form>
                    <div class='uk-margin'>    
                        
                        <input class="uk-input uk-border-pill uk-form-width-large"   v-model="recipe.name" placeholder="It should sound delicious!" >
                        
                    </div>
                </form>
            </div>
        </div>
    </div>
  <div class="uk-container uk-container-small">
        <div class="uk-grid-large" data-uk-grid>
            <div class="uk-width-expand@m">
                <div class="uk-article">
                    
                    <h3>3 - Steps: </h3>
                    <form>
                        <div class='uk-margin'>    
                            <div class="uk-inline">
                                <a class="uk-form-icon uk-form-icon-flip" uk-icon="icon: plus-circle" @click="add_step(step_detail)"></a>
                                <input class="uk-input uk-border-pill uk-form-width-large" type="text" v-model="step_detail" placeholder="Tell us how to make this meal step by step"></input>
                            </div>
                        </div>

                    </form>

                    <div v-for="(step,index)  in recipe.steps"  class="uk-grid-small uk-margin-medium-top" data-uk-grid>
                        <div class="uk-width-auto">
                        <a href="#" class="uk-step-icon" data-uk-icon="icon: check; ratio: 0.8" 
                            data-uk-toggle="target: #step-1; cls: uk-step-active"></a>
                        </div>
                            <div class="uk-width-expand">
                            <h5 class="uk-step-title uk-text-500 uk-text-uppercase uk-text-primary" data-uk-leader="fill:—">{{index +1}}. Step</h5>
            
                            <form>
                                <div class='uk-margin'>    
                                    <div class="uk-inline">
                                        <a class="uk-form-icon uk-form-icon-flip" uk-icon="icon: ban" @click="remove_step(step)"></a>
                                        <input class="uk-input uk-border-pill uk-form-width-large" type="text" v-model = "recipe.steps[index].step" ></input>
                                    </div>
                                </div>

                            </form>
                        </div>
                    </div>

                </div>
            </div>

            <div class="uk-width-1-3@m">
                <h3>4 - Ingredients</h3>
                <form>
                    <div class='uk-margin'>    
                        <div class="uk-inline">
                            <a class="uk-form-icon uk-form-icon-flip" uk-icon="icon: plus-circle" @click="add_ingredient(input_ingredient)"></a>
                            <input class="uk-input uk-border-pill uk-form-width-large" type="text"  v-model="input_ingredient" placeholder="Add ingredients" ></input>
                        </div>
                    </div>

                </form>
                <ul v-for="(ingredient,index) in recipe.ingredients" class="uk-list uk-list-large uk-list-divider uk-margin-medium-top">
                    <li >
                        <h5 class="uk-step-title uk-text-500 uk-text-uppercase uk-text-primary" data-uk-leader="fill:—">{{index +1}}.{{show_cate[index]}}</h5>
                        <form>
                            <div class='uk-margin'>    
                                <div class="uk-inline">
                                    <a class="uk-form-icon uk-form-icon-flip" uk-icon="icon: ban" @click="remove_ingredient(ingredient),remove_cate(index)"></a>
                                    <input class="uk-input uk-border-pill uk-form-width-large" type="text" v-model = "recipe.ingredients[index]">
                                </div>
                            </div>

                        </form>
                    </li>
    
                </ul>
            </div>



        </div>


    </div>
    <div class="uk-container uk-container-small">
        <div class="uk-grid-large" data-uk-grid>
            <div class="uk-width-expand@m">
                <h3>5 - Tags:</h3>
                <form>
                    <div class='uk-margin'>    
                        <div class="uk-inline">
                            <a class="uk-form-icon uk-form-icon-flip" uk-icon="icon: plus-circle" @click="add_tag(input_tag)"></a>
                            <input class="uk-input uk-border-pill uk-form-width-large" type="text"  v-model="input_tag" placeholder="Add Tags" ></input>
                        </div>
                    </div>
                </form>
                    <div class="uk-margin-medium-top" data-uk-margin>
                        <a class="uk-display-inline-block" @click="remove_tag(tag)" v-for="tag in recipe.tags"><span class="uk-label uk-label-light">{{tag}}</span></a>
                    </div>
            </div>
            <div class="uk-width-1-3@m">
                <h3>6 - MealType:</h3>
                <div class="uk-form-controls">
                    <select class="uk-select" id="form-stacked-select" v-model="recipe.MealType">
                        <option>BREAKFAST</option>
                        <option>DINNER</option>
                        <option>LUNCH</option>
                        <option>DESSERT</option>
                    </select>
                </div>
            </div>
        </div>
    </div>

    <div class="uk-container uk-container-small">
        <div class="uk-grid-large" data-uk-grid>
            <div class="uk-width-expand@m">
                <h3>7 - Total time needed(mins):</h3>
                <form>
                    <div class='uk-margin'>    
                        
                        <input class="uk-input uk-border-pill uk-form-width-large"   v-model="recipe.time" placeholder="How long does it take to make this meal(mins)" ></input>
                        
                    </div>
                </form>

            </div>
            <div class="uk-width-1-3@m">
                <h3>8 - Serve sizes:</h3>
                <form>
                    <div class='uk-margin'>    
                        
                        <input class="uk-input uk-border-pill uk-form-width-large"   v-model="recipe.serves" placeholder="How many people can this meal feed" ></input>
                        
                    </div>
                </form>
            </div>
        </div>
    </div>


    <div class="uk-container uk-container-small">
        <div class="uk-grid-large" data-uk-grid>
            <div class="uk-width-expand@m">
                <h3>9 - Image:</h3>
                
            <div class="uk-margin" uk-margin>
                <div uk-form-custom="target: true">
                    <input type="file" @change="upload">
                    <input class="uk-input uk-form-width-medium" type="text" placeholder="Select file" disabled>
                </div>
            </div>
               
                    


            </div>

        </div>
    </div>

    <br>
    <div class="uk-flex uk-flex-center">
        <a class="uk-button uk-button-primary uk-button-large uk-width-1-4" @click="submit_recipe">Save</a>
    </div>


</div>

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
        return { // steps 里面需要有step， 还需要给我mealtype，// save用户信息 // save recipe 更新后的信息
            recipe:{
                name:'',
                img:"",
                description:'',
                time: 0,
                serves:0,
                author:'Steve',
                ingredients:[],
                steps:[],
                tags:[],
                MealType:'Breakfast'
            },
            number_steps:1,
            step_detail:'',
            input_ingredient:'',
            input_tag:'',
            user_id: -1,
            recipe_id:-1,
            show_cate:[]
       
            
        }
    },  
    mounted() {
        
        this.user_id= this.$my_window.getItem('user_id')
        this.recipe_id=this.$my_window.getItem('recipe_id')
        console.log("user id is" +this.user_id);
        this.init(this.recipe_id)

    },  
    methods:{
        remove_cate(index){
            this.show_cate.splice(index,1)

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
        submit_recipe(){
            console.log("delete")
            this.$http.delete("recipe/delete_recipe",{params:{id:this.recipe_id}}).then(res => {  
                console.log("delete")
                })

            const params = new URLSearchParams();
            params.append('name',this.recipe.name)
            params.append('img',this.recipe.img)
            params.append('description',this.recipe.description)
            params.append('time',this.recipe.time)
            params.append('serves',this.recipe.serves)
            params.append('ingredients',this.recipe.ingredients)
            params.append('steps',JSON.stringify(this.recipe.steps))
            params.append('tags',this.recipe.tags)
            params.append('mealtype',this.recipe.MealType)
            params.append('author',this.recipe.author)
            params.append('user_id',this.user_id)
            
            

            this.$http.post("recipe/create_recipe",params).then(
                res => {

                    this.$message({
                        message: 'Changes saved',
                        type: 'success'
                    })
                }
            ).catch(err =>{
                console.log(err.response)
            })

        },
        goto_signup()
        {
          this.$router.push("/SignUp")
        },
        goto_login(){
          this.$router.push("/login")
        },
        go_to_profile()
        {
          if(this.user_id == null || this.user_id == -1)
          {
            this.$message({
							message: 'Please sigin or create account',
							type: 'warning'
						});
          }else
          {
            this.$router.push("/profile")
          }
        },

        add_step(step){
            this.recipe.steps.push({"step":step})

        },
        remove_step(step){
            this.recipe.steps.splice(this.recipe.steps.indexOf(step),1)
        },
        add_ingredient(input_ingredient){
            this.$http.get("ingredient/get_category_by_ingredient",{params:{ingredient_name:input_ingredient}}).then( res => {
                if(res.status == 200)
                {
                    this.show_cate.push(res.data);
                    this.recipe.ingredients.push(input_ingredient)
                }
            }).catch(err => {
                if(err.response.status == 404)
                {
						this.$message({
							message: 'Please try other ingredients',
							type: 'warning'
						});                    
                }
            })
        },
        remove_ingredient(ingredient){
            this.recipe.ingredients.splice(this.recipe.ingredients.indexOf(ingredient),1)
        },
        add_tag(tag){
            this.recipe.tags.push(tag)
        },
        remove_tag(tag){
            this.recipe.tags.splice(this.recipe.tags.indexOf(tag),1)
        },
        init(input_recipe_id){
            this.$http.get("recipe",{params:{id:input_recipe_id}}).then(res => {
                console.log(res.data)
                this.recipe = res.data
                 this.recipe.steps =JSON.parse(this.recipe.steps)
                 var x
                 for(x of res.data.ingredients)
                 {
                     console.log(x)
                     this.$http.get("ingredient/get_category_by_ingredient",{params:{ingredient_name:x}}).then( result => {
                         this.show_cate.push(result.data)
                     })
                 }
            })
        },
        go_to_home(){
            this.$router.push("/home")
        },
        upload(event){
            // console.log(event.target.files[0].name)
            this.recipe.img = event.target.files[0].name
            console.log(this.recipe.img)

        },
        Signup(){
          this.$router.push('/SignUp');
        },
    }
}
</script>>

