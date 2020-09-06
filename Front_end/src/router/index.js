import Vue from 'vue'
import VueRouter from 'vue-router'
import new_Login from '../components/new_Login.vue'
import new_SignUp from '../components/new_SignUp'
import new_Home from '../components/new_Home'
import recipe from '../components/recipe'
import create_recipe from '../components/create_recipe'
import profile from '../components/profile'
import edit from '../components/edit_recipe'
Vue.use(VueRouter)

  const routes = [
	  	{
		  path:'/login',
		  component:new_Login
	 	},
	  	{
		  path:'/',
		  redirect:'/login'
	  	},
	  	{
		  path:'/SignUp',
		  component:new_SignUp
	 	},
	  	{
		  path:'/home',
		  component: new_Home
	  	},
		{
			path:'/recipe',
			component:recipe
		},
		{
			path:'/create_recipe',
			component:create_recipe
		},
		{
			path:'/profile',
			component:profile
		},
		{
			path:'/edit_recipe',
			component: edit
		}

  
]

const router = new VueRouter({
  routes
})

export default router
