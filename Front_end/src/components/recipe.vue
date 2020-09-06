<template>
    
<div>

<nav class="uk-navbar-container uk-letter-spacing-small">
  <div class="uk-container">
    <div class="uk-position-z-index" data-uk-navbar>
      <div class="uk-navbar-left">
        <a class="uk-navbar-item uk-logo" @click="go_to_home">MealMatch</a>

      </div>
      <div class="uk-navbar-right">
        <!-- <div>
          <a class="uk-navbar-toggle" data-uk-search-icon href="#"></a>
          <div class="uk-drop uk-background-default" data-uk-drop="mode: click; pos: left-center; offset: 0">
            <form class="uk-search uk-search-navbar uk-width-1-1">
              <input class="uk-search-input uk-text-demi-bold" type="search" placeholder="Search..." autofocus>
            </form>
          </div>
        </div> -->
        <ul class="uk-navbar-nav uk-visible@m">
          <li><a uk-icon="user"  @click="go_to_profile"></a><li>
          <li ><a @click="goto_login">Sign In</a></li>
          <li ><a @click="create_recipe">Create Recipe</a></li>
        </ul>
        <div  class="uk-navbar-item">
          <div><a class="uk-button uk-button-primary" @click="$router.push('/SignUp')">Sign Up</a>
          </div>
        </div>          
        <a class="uk-navbar-toggle uk-hidden@m" href="#offcanvas" data-uk-toggle><span
          data-uk-navbar-toggle-icon></span></a>
      </div>
    </div>
  </div>
</nav>

<div class="uk-container">
  <div data-uk-grid>
    <div class="uk-width-1-2@s">
      <div><img class="uk-border-rounded-large" :src="getImgUrl(recipe.img)" 
        alt="Image alt"></div>
    </div>
    <div class="uk-width-expand@s uk-flex uk-flex-middle">
      <div>
        <h1>{{recipe.name}}</h1>
        <p>{{recipe.description}}</p>
        <div class="uk-margin-medium-top uk-child-width-expand uk-text-center uk-grid-divider" data-uk-grid>

          <div>
            <span data-uk-icon="icon: future; ratio: 1.4"></span>
            <h5 class="uk-text-500 uk-margin-small-top uk-margin-remove-bottom">Total Time</h5>
            <span class="uk-text-small">{{recipe.time}}</span>
          </div>
          <div>
            <span data-uk-icon="icon: users; ratio: 1.4"></span>
            <h5 class="uk-text-500 uk-margin-small-top uk-margin-remove-bottom">Yield</h5>
            <span class="uk-text-small">Serves {{recipe.serves}}</span>
          </div>
        </div>
        <hr>
        <div data-uk-grid>
          <div class="uk-width-auto@s uk-text-small">
            <p class="uk-margin-small-top uk-margin-remove-bottom">Created by <a >{{recipe.author}}</a></p>
          </div>
          <div class="uk-width-expand@s uk-flex uk-flex-middle uk-flex-right@s">
            <!-- <a href="#" class="uk-icon-link" data-uk-icon="icon: plus-circle; ratio: 1.2" 
             data-uk-tooltip="title: Save Recipe"></a> -->
            <a @click="edit_recipe" class="uk-icon-link uk-margin-left" data-uk-icon="icon: settings; ratio: 1.2" 
             data-uk-tooltip="title: edit recipe"></a>
            <!-- <a href="#" class="uk-icon-link uk-margin-left" data-uk-icon="icon: print; ratio: 1.2" 
             data-uk-tooltip="title: Print Recipe"></a> -->
          </div>
        </div>
      </div>
    </div>
  </div>
</div>

<div class="uk-section uk-section-default">
  <div class="uk-container uk-container-small">
    <div class="uk-grid-large" data-uk-grid>
      <div class="uk-width-expand@m">
        <div class="uk-article">
          <h3>How to Make It</h3>

            <div v-for="(step,index)  in recipe.steps"  class="uk-grid-small uk-margin-medium-top" data-uk-grid>
                <div class="uk-width-auto">
                <a  id="step" class="uk-step-icon" data-uk-icon="icon: check; ratio: 0.8" 
                    data-uk-toggle="target: #step; cls: uk-step-active"></a>
                </div>
                <div class="uk-width-expand">
                <h5 class="uk-step-title uk-text-500 uk-text-uppercase uk-text-primary" data-uk-leader="fill:—">{{index+1}}. Step</h5>
                <div class="uk-step-content">{{recipe.steps[index].step}}</div>
                </div>
            </div>


          <hr class="uk-margin-medium-top uk-margin-large-bottom">
          <h3>Comments</h3>
          <ul class="uk-comment-list uk-margin-medium-top">
            <li>
              <article class="uk-comment uk-visible-toggle" tabindex="-1">
                <header class="uk-comment-header uk-position-relative">
                  <div class="uk-grid-medium uk-flex-middle" data-uk-grid>
                    <div class="uk-width-auto">
                      <img class="uk-comment-avatar uk-border-circle" src="https://via.placeholder.com/100x100" width="50" height="50" alt="Alice Thomson">
                    </div>
                    <div class="uk-width-expand">
                      <h4 class="uk-comment-title uk-margin-remove"><a class="uk-link-reset" href="#">Alice Thomson</a></h4>
                      <p class="uk-comment-meta uk-margin-remove"><a class="uk-link-reset" href="#">12 days ago</a></p>
                      <div class="uk-rating">
                        <span class="uk-rating-filled" data-uk-icon="icon: star; ratio: 0.8"></span>
                        <span class="uk-rating-filled" data-uk-icon="icon: star; ratio: 0.8"></span>
                        <span class="uk-rating-filled" data-uk-icon="icon: star; ratio: 0.8"></span>
                        <span class="uk-rating-filled" data-uk-icon="icon: star; ratio: 0.8"></span>
                        <span data-uk-icon="icon: star; ratio: 0.8"></span>
                      </div>
                    </div>
                  </div>
                  <div class="uk-position-top-right uk-position-small uk-hidden-hover"><a class="uk-link-muted" href="#">Reply</a>
                  </div>
                </header>
                <div class="uk-comment-body">
                  <p>I love it</p>
                </div>
              </article>
              <ul>
                <li>
                  <article class="uk-comment uk-comment-primary uk-visible-toggle uk-border-rounded" tabindex="-1">
                    <header class="uk-comment-header uk-position-relative">
                      <div class="uk-grid-medium uk-flex-middle" data-uk-grid>
                        <div class="uk-width-auto">
                          <img class="uk-comment-avatar uk-border-circle" src="https://via.placeholder.com/100x100" width="50" height="50" alt="Tom Solender">
                        </div>
                        <div class="uk-width-expand">
                          <h4 class="uk-comment-title uk-margin-remove"><a class="uk-link-reset" href="#">Tom Solender</a></h4>
                          <p class="uk-comment-meta uk-margin-remove-top"><a class="uk-link-reset" href="#">12 days ago</a></p>
                        </div>
                      </div>
                      <div class="uk-position-top-right uk-position-small uk-hidden-hover"><a class="uk-link-muted"
                          >Reply</a></div>
                    </header>
                    <div class="uk-comment-body">
                      <p>nice meal</p>
                    </div>
                  </article>
                </li>

              </ul>
            </li>
          </ul>
        </div>
      </div>
      <div class="uk-width-1-3@m">
        <h3>Ingredients</h3>
        <ul  class="uk-list uk-list-large uk-list-divider uk-margin-medium-top">
          <li v-for="ingredient in recipe.ingredients">{{ingredient}}</li>
          
        </ul>
        <h3 class="uk-margin-large-top">Tags</h3>
        <div class="uk-margin-medium-top" data-uk-margin>
          <a class="uk-display-inline-block"  v-for="tag in recipe.tags"><span class="uk-label uk-label-light">{{tag}}</span></a>
         
        </div>
        <h3 class="uk-margin-large-top">Share Recipe</h3>
        <div class="uk-margin-medium-top">
          <div data-uk-grid class="uk-child-width-auto uk-grid-small">
            <div>
              <a href="#" data-uk-icon="icon: facebook; ratio: 0.9" class="uk-icon-button facebook" target="_blank"></a>
            </div>
            <div>
              <a href="#" data-uk-icon="icon: linkedin; ratio: 0.9" class="uk-icon-button linkedin" target="_blank"></a>
            </div>
            <div>
              <a href="#" data-uk-icon="icon: twitter; ratio: 0.9" class="uk-icon-button twitter" target="_blank"></a>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</div>

<div class="uk-section uk-section-muted">
  <div class="uk-container">
    <h3>Other Recipes You May Like</h3>
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
      
   
  </div>
</div>

<footer class="uk-section uk-section-default">
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
export default {
    data() {
        return {
            recipe:{
                name:'potato beef',
                img:"https://www.diabetes.co.uk/wp-content/uploads/2019/01/What-to-eat-on-a-ketogenic-diet.png",
                description:'very nice meal',
                time: 15,
                serves:3,
                author:'aaaa',
                ingredients:['tomato'],
                steps:['boil'],
                tags:['HEALTHY']
            },
            recipe_id:-1,
            user_id: -1,
            username:"none",
            show_change_button:false,
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
            ]
        }
    },
    mounted() {
    
        console.log('button'+this.show_change_button)
        this.recipe_id = this.$my_window.getItem('recipe_id');
        this.user_id = this.$my_window.getItem('user_id');
        this.init(this.recipe_id);
        this.find_username(this.user_id)
        this.random_recipe()
        
    },

    methods:{
            random_recipe(){
          this.$http.get("random_recipe").then( res =>{
            console.log(res.data)
            this.recipes_list = res.data
            
          })
        },
        go_to_home(){
            this.$router.push("/home")
        },
        edit_recipe(){
            
            if(this.username == this.recipe.author)
            {
              this.$router.push("/edit_recipe")
            }else{
              this.$message({
							message: 'You have no permission to edit this recipe',
							type: 'warning'
						});
            }
            console.log(this.username)

        },
        init(input_recipe_id){
            this.$http.get("recipe",{params:{id:input_recipe_id}}).then(res => {
                console.log(res.data)
                this.recipe = res.data
                this.recipe.steps =JSON.parse(this.recipe.steps)
            })
        },
        find_username(input_user_id){
                this.$http.get("get_user_name",{params:{id:input_user_id}}).then( res => {
                  this.username =res.data
            })
        },
        check_ownerShip(){
          if(this.username == this.recipe.author)
          {
            this.show_change_button = true;
          }else
          {
            this.show_change_button = false;
          }

        },
        getImgUrl(pic) {
            if(pic != "")
            {
                return require('../assets/img/'+pic)
            }
            return require('../assets/img/mango.png')
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
        }
    }
}
</script>