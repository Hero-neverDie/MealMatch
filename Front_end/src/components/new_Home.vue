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
                        <div><a class="uk-button uk-button-primary" @click="goto_signup">Sign Up</a></div>
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
          <h1 class="uk-heading-small uk-margin-remove-top">Choose from thousands of recipes</h1>
          <p class="uk-text-secondary">Cooking is no longer difficult</p>
          <a class="uk-logo  hvr-forward " style="color:#EB4A36; " @click="Signup">Sign up today<span
            class="uk-margin-small-left" data-uk-icon="arrow-right"></span></a>
        </div>
      </div>
      <div class="uk-width-expand@m">
      </div>
    </div>
  </div>
</div>

<div class="uk-section uk-section-default">
  <div class="uk-container">
    <div data-uk-grid>
      <div class="uk-width-1-4@m sticky-container">
        <div data-uk-sticky="offset: 100; bottom: true; media: @m;">
        <h2>Recipes</h2>
          <ul class="uk-nav-default uk-nav-parent-icon uk-nav-filter uk-margin-medium-top" data-uk-nav>
            <li class="uk-parent ">
              <a href="#">Meal Type</a>
              <ul class="uk-nav-sub" >
                    <li v-for="type in mealType" ><a @click="add_mealtype(type)">{{type}}</a></li>
              </ul>
            </li>
            <template v-for="(object,index) in Ingrediants">
              <li v-for="(value,name) in object" class="uk-parent">
                <a href="#">{{name}}</a>
                <ul  class="uk-nav-sub">
                      <li v-for="item in value"><a @click="add_ingrediants(item.name),find_suggestion()">{{item.name}}</a></li> 
                </ul>
              </li>
            </template>


          </ul>


        </div>
      </div>
            <div v-show="show_list" class="uk-card uk-card-default uk-card-body uk-width-1-4@m" style="position:absolute;width:13%; transform:translate(-90%,10%);">
                <h3 class="uk-card-title">MealType:</h3>
                <ul>
                    <li v-for="type in checkList.meal_Type"><a @click="remove_mealtype(type)">{{type}}</a></li>
                </ul>
              
                <h3 class="uk-card-title">Ingredients:</h3>
                <ul>
                    <li v-for="item in checkList.Ingrediants"><a @click="remove_ingrediants(item)">{{item}}</a></li>
                </ul>

                <form class="uk-search uk-search-default uk-width-1-1">
                <a data-uk-search-icon @click="add_ingrediants(user_input)"></a>
                <input v-model="user_input" class="uk-search-input uk-text-small uk-border-rounded uk-form-medium" type="search" placeholder="apple?">
                </form>

                <h3 class="uk-card-title">Suggestion:</h3>  
                <ul>
                    <li><a @click="add_ingrediants(suggestion),find_suggestion()">{{suggestion}}</a></li>
                </ul> 
            </div>
      <div class="uk-width-expand@m">
        <div data-uk-grid>
          <div class="uk-width-expand@m">
            <form class="uk-search uk-search-default uk-width-1-1">
              <a data-uk-search-icon @click="search_recipe(search_recipe_name)"></a>
              <input v-model='search_recipe_name' class="uk-search-input uk-text-small uk-border-rounded uk-form-large" type="search" placeholder="Search for recipes...">
            </form>          
          </div>

        </div>      

        <div  class="uk-child-width-1-2 uk-child-width-1-3@s" data-uk-grid>
          <div v-for="object in Recipes_list">
            <div  class="uk-card">
              <div class="uk-card-media-top uk-inline uk-light">
                <img class="uk-border-rounded-medium" :src="getImgUrl(object.img)" alt="Course Title" style="width:250px; height:180px;">
                <div class="uk-position-cover uk-card-overlay uk-border-rounded-medium"></div>
                <div class="uk-position-xsmall uk-position-top-right">
                  <a href="#" class="uk-icon-button uk-like uk-position-z-index uk-position-relative"
                    data-uk-icon="heart"></a>
                </div>
              </div>
              <div>
                <h3 class="uk-card-title uk-text-500 uk-margin-small-bottom uk-margin-top">{{object.name}}</h3>
                <div class="uk-text-xsmall uk-text-muted" data-uk-grid>
                  <div class="uk-width-auto uk-flex uk-flex-middle">
                    <span class="uk-rating-filled" data-uk-icon="icon: star; ratio: 0.7"></span>
                    <span class="uk-margin-xsmall-left">{{object.rating}}</span>
                  </div>
                  <div class="uk-width-expand uk-text-right">{{object.author}}</div>
                </div>
              </div>
              <a @click="add_recipe_id(object.id)" class="uk-position-cover"></a>
            </div>
          </div>
        </div>

        
      </div>
    </div>
  </div>
</div>


<br>
<br>
<br>
<br>
<br>
<div class="uk-section uk-section-default">
  <div class="uk-container">
    <div data-uk-grid>
      <div class="uk-width-expand">
        <h2>Videos</h2>          
      </div>

    </div >      
    <div class="uk-child-width-1-2 uk-child-width-1-4@s" data-uk-grid>
      <div style="width:300px,height:200px">
        <div
          class="uk-card uk-card-video">
          <div class="uk-inline uk-light">
            <img class="uk-border-rounded-large" src="https://3.bp.blogspot.com/-HGGd4MjBVlA/WBDsgi2S0DI/AAAAAAAAFE8/JsYOmh8VoWAQsJXKmkLXBSLFac7lD8QuQCLcB/s280/hellskitchen.JPG" alt="Course Title">
            <div class="uk-position-cover uk-card-overlay uk-border-rounded-large"></div>
            <div class="uk-position-center">
              <span data-uk-icon="icon: play-circle; ratio: 3.4"></span>
            </div>
            <div class="uk-position-small uk-position-bottom-left">
              <h5 class="uk-margin-small-bottom">most friendly chef in the world</h5>
              <div class="uk-text-xsmall">by Gordan Ramsy</div>
            </div>
          </div>
          <a href="https://www.youtube.com/watch?v=0eF5wn0QeZs" class="uk-position-cover"></a>
        </div>
      </div>
      <div style="width:300px,height:200px">
        <div class="uk-card uk-card-video" >
          <div class="uk-inline uk-light">
            <img class="uk-border-rounded-large" src="https://www.pluggedin.com/wp-content/uploads/2020/01/hells-kitchen.jpg" alt="Course Title">
            <div class="uk-position-cover uk-card-overlay uk-border-rounded-large"></div>
            <div class="uk-position-center">
              <span data-uk-icon="icon: play-circle; ratio: 3.4"></span>
            </div>
            <div class="uk-position-small uk-position-bottom-left">
              <h5 class="uk-margin-small-bottom">Eat my sandwich</h5>
              <div class="uk-text-xsmall">by Gordan Ramsy</div>
            </div>
          </div>
          <a href="https://www.youtube.com/watch?v=5er2tOyMYIk" class="uk-position-cover"></a>
        </div>
      </div>
      <div >
        <div
          class="uk-card uk-card-video">
          <div class="uk-inline uk-light" >
            <img  class="uk-border-rounded-large" src="https://3.bp.blogspot.com/-HGGd4MjBVlA/WBDsgi2S0DI/AAAAAAAAFE8/JsYOmh8VoWAQsJXKmkLXBSLFac7lD8QuQCLcB/s280/hellskitchen.JPG" alt="Course Title">
            <div class="uk-position-cover uk-card-overlay uk-border-rounded-large"></div>
            <div class="uk-position-center">
              <span data-uk-icon="icon: play-circle; ratio: 3.4"></span>
            </div>
            <div class="uk-position-small uk-position-bottom-left">
              <h5 class="uk-margin-small-bottom">Eat my steak</h5>
              <div class="uk-text-xsmall">by Gordan Ramsy</div>
            </div>
          </div>
          <a href="https://www.youtube.com/watch?v=CaO2mQKyAX0" class="uk-position-cover"></a>
        </div>
      </div>
      <div>
        <div
          class="uk-card uk-card-video">
          <div class="uk-inline uk-light">
            <img class="uk-border-rounded-large" src="https://www.pluggedin.com/wp-content/uploads/2020/01/hells-kitchen.jpg" alt="Course Title">
            <div class="uk-position-cover uk-card-overlay uk-border-rounded-large"></div>
            <div class="uk-position-center">
              <span data-uk-icon="icon: play-circle; ratio: 3.4"></span>
            </div>
            <div class="uk-position-small uk-position-bottom-left">
              <h5 class="uk-margin-small-bottom">best cook in the world</h5>
              <div class="uk-text-xsmall">by Gordan Ramsy</div>
            </div>
          </div>
          <a href="https://www.youtube.com/watch?v=UxEKMQUvWLc" class="uk-position-cover"></a>
        </div>
      </div>      
    </div>
  </div>
</div>

<div class="uk-container">
  <div class="uk-background-primary uk-border-rounded-large uk-light">
    <div class="uk-width-3-4@m uk-margin-auto uk-padding-large">
      <div class="uk-text-center">
        <h2 class="uk-h2 uk-margin-remove">Be the first to know about the latest deals, receive new trending recipes &amp; more!</h2>
      </div>
      <div class="uk-margin-medium-top">
        <div data-uk-scrollspy="cls: uk-animation-slide-bottom; repeat: true">
          <form>
            <div class="uk-grid-small" data-uk-grid>
              <div class="uk-width-1-1 uk-width-expand@s uk-first-column">
                <input type="email" placeholder="Email Address" class="uk-input uk-form-large uk-width-1-1 uk-border-pill">
              </div>
              <div class="uk-width-1-1 uk-width-auto@s">
                <input @click="$message({
							message: 'Email received',
							type: 'success'
						})" type="submit" value="Subscribe" class="uk-button uk-button-large uk-button-warning">
              </div>
            </div>
          </form>
        </div>
      </div>
    </div>
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

<script>

import "../assets/js/uikit.js"
export default {
    data() {
        return {
            Ingrediants:[
                {vegetables: [
                    { name: 'cabbage'},
                    { name: 'carrot'},
                    {name:'potato'}
                ]},
                {meat: [
                    { name: 'beef' },
                    { name: 'chicken'},
                    {name:'lamb'},
                    {name:'Pork'}
                ]},
                {fruits: [
                    { name: 'apple'},
                    { name: 'pear' },
                    {name:'watermelon'},
                    {name:'Banana'}
                ]}
            ],
            mealType:['Breakfast','Lunch',"Dinner","Dessert"], // used

            search_recipe_name:'',
            checkList: { //used
                meal_Type:[],
                Ingrediants:[]
            },
            user_input:'',
            show_list:false, //used
            suggestion:'', //used
            user_id: -1,

            Recipes_list:[

   

            ],
            
        }
    },
    mounted(){

      this.retrive_ingrediants()
      this.retrive_mealType()
      this.user_id =this.$my_window.getItem('user_id')
      this.random_recipe()
      },

    methods: {

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
        goto_signup()
        {
          this.$router.push("/SignUp")
        },
        retrive_mealType(){
          this.$http.get('recipe/get_meal_type').then( res=>{
            console.log(res.data)
            this.mealType = res.data
          })
        },
        retrive_ingrediants(){
          this.$http.get('ingredient/get_all').then( res => {
            this.Ingrediants = res.data
          })
        },
        add_mealtype: function(mealType){
            if(this.checkList.meal_Type.indexOf(mealType) == -1)
            {
                this.checkList.meal_Type.push( mealType);
            }
            this.show_list = true;
            this.send_ingrediant_mealType()
            
        },
        remove_mealtype: function(mealType){
             this.checkList.meal_Type.splice(this.checkList.meal_Type.indexOf(mealType),1)
             this.send_ingrediant_mealType()
        },
        add_ingrediants: function(item){
            if(this.checkList.Ingrediants.indexOf(item) == -1)
            {
                this.checkList.Ingrediants.push(item)
            }
            this.show_list = true;

            this.send_ingrediant_mealType()

            
        },

        send_ingrediant_mealType(){
          const params = new URLSearchParams();
          params.append('meal_Type',this.checkList.meal_Type)
          params.append('Ingredients',this.checkList.Ingrediants)
        
            this.$http.post('recipe/get_recipes',params).then( res => {
              console.log(res)
              this.Recipes_list = res.data
            }).catch(err =>{

              this.Recipes_list = []


            })
        },
        search_recipe: function(name_recipe){
          this.$http.get('recipe/search_by_name', {params:{recipe_name:name_recipe}}).then(res => {
            this.Recipes_list = res.data
          }).catch(err => {
              this.$message({
                message: 'recipe not found',
                type: 'warning'
              });
            
          })
          
        },
        remove_ingrediants: function(item){
            this.checkList.Ingrediants.splice(this.checkList.Ingrediants.indexOf(item),1)
            this.send_ingrediant_mealType()
        },
        remove_item: function(item){
            this.checkList.splice(this.checkList.indexOf(item),1)
        },
        add_item:function(item){
            var i;
            var subject = true;
            for(i = 0; i< this.Ingrediants.length; i++)
            {
                for( var key in this.Ingrediants[i])
                {
                    this.Ingrediants[i][key].forEach(e =>{
                        if(e.name === item)
                        {
                            if(this.checkList.Ingrediants.indexOf(item) == -1)
                            {
                                this.checkList.Ingrediants.push(item)
                            }
                            subject = false
                            console.log(e);
                            return;
                        }
                    })
                }
            }
            if(subject)
            {
              this.$message({
                message: 'Please try other ingredients',
                type: 'warning'
              });
                
            }

            // alert('Ingrediant not found');
            
          
        },

        find_suggestion: function(){
          const params = new URLSearchParams();
          console.log(this.checkList.meal_Type)
          console.log(this.checkList.Ingrediants)
          
          params.append('meal_Type',this.checkList.meal_Type)
          params.append('Ingredients',this.checkList.Ingrediants)
        
            this.$http.post('recipe/recommend_ingredients',params).then( res => {
              console.log("suggestion "+res.data)
              this.suggestion = res.data
            }).catch(err =>{})

        //  "vegetables",
    // "meats",
    // "dairy",
    // "fruits",
    // "seafood"


        },

        Signup(){
          this.$router.push('/SignUp');
        },
        add_recipe_id: function(id){
          if(this.user_id == null || this.user_id == -1)
          {
            this.$message({
							message: 'Please sigin or create account',
							type: 'warning'
            });
          }else{
            this.$my_window.setItem('recipe_id',id)
            this.$router.push('/recipe');
          }
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
        random_recipe(){
          this.$http.get("random_recipe").then( res =>{
            console.log(res.data)
            this.Recipes_list = res.data
            console.log("in random"+ JSON.stringify(this.Recipes_list))
          })
        }
    },
}
</script>




<style lang="less" scoped>

    @import '../assets/css/main.css';
    @import url("https://fonts.googleapis.com/css?family=Montserrat:400,500,600&display=swap");
    @import url("https://fonts.googleapis.com/css?family=Leckerli+One&display=swap");


.right_box{
    transform: translate(90%,-80%);
}

.left_box{
    transform: translate(0,17%);
}

.big_box{
    transform: translate(0,-8%);
}


  .text {
    font-size: 14px;
  }

  .item {
    margin-bottom: 18px;
  }

  .clearfix:before,
  .clearfix:after {
    display: table;
    content: "";
  }
  .clearfix:after {
    clear: both
  }

  .box-card {
    width: 480px;
  }

</style>










