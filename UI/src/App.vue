<template>

    <div id="app">
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">





        <router-view @authenticated="setAuthenticated" />
    </div>
</template>

<script>
    import axios from 'axios';
    import MultipleFileUploader from '@updivision/vue2-multi-uploader';

    var modal = document.getElementById('id01');

    window.onclick = function(event) {
        if (event.target == modal) {
            modal.style.display = "none";
        }
    }

    window.onload = function() {
        var this_ = this;
        document.getElementsByClassName('uploadBox')[0].__vue__.$props.postHeader = {Authorization: "Token " + localStorage.token};
    }

    export default {
        name: 'App',
        data() {
            return {
                authenticated: false,
                token: undefined,
            }
        },
        components: {
            MultipleFileUploader
        },
        mounted() {
            if (localStorage.hasOwnProperty('token')) {
                this.token = localStorage.token;
                this.authenticated = true;
            }
            if(!this.authenticated) {
                this.$router.replace({ name: "login" });
            }
            else {
                var this_ = this;
                this.$router.replace({name: "secure"});
            }
        },
        methods: {
            updateToken () {
                document.getElementsByClassName('uploadBox')[0].__vue__.$props.postHeader = {Authorization: "Token " + localStorage.token};
            },
            setAuthenticated(status) {
                this.authenticated = status;
            },
            logout() {
                var this_ = this;
                axios.post('/api/sign_out/', {Authorization: "Token " + String(this.token)}).then(function () {
                    this_.authenticated = false;
                    this_.$router.replace({ name: "login" });
                    delete localStorage.token;
                });
            }
        },
    }
</script>

<style>
    body {
        background-color: #E0E0E0;
        background-image: url("background.jpg");
    }
    h1 {
        padding: 0;
        margin-top: 0;
    }
    #app {
    }

    .active {
        background-color: #4CAF50;
        color: white;
    }

    button:hover {
      opacity: 0.8;
    }

    .dropAreaDragging{
        background-color: #ccc;
    }

    .searchbar{
        margin: auto;
        height: 60px;
        background-color: #353b48;
        border-radius: 30px;
        padding: 10px;
    }

    .search_input{
        color: white;
        border: 0;
        outline: 0;
        background: none;
        width: 0;
        line-height: 40px;
        transition: width 0.4s linear;
    }

    .searchbar:hover > .search_input{
        padding: 0 10px;
        width: 200px;
        transition: width 0.4s linear;
    }

    .searchbar:hover > .search_icon{
        background: white;
        color: #e74c3c;
    }

    .search_icon{
        height: 40px;
        width: 40px;
        float: right;
        display: flex;
        justify-content: center;
        align-items: center;
        border-radius: 50%;
        color:white;
    }
</style>