<template>

    <div id="app">
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
        
        <b-navbar toggleable="md" type="dark" v-if="authenticated" variant="info" sticky="true">

          <b-navbar-toggle target="nav_collapse"></b-navbar-toggle>

          <b-navbar-brand href="photoclo.ru:8000">PHOTOCLO</b-navbar-brand>

          <b-collapse is-nav id="nav_collapse" right>

            <b-navbar-nav class="ml-auto">

              <div class="container h-100">
              <div class="d-flex justify-content-center h-100">
                <div class="searchbar">
                  <input class="search_input" type="text" name="" placeholder="Search...">
                  <a href="#" class="search_icon"><i class="fas fa-search"></i></a>
                </div>
              </div>
            </div>

              <b-button v-b-modal.uploadModal v-on:click='updateToken()' right>Загрузить</b-button>

                <b-modal id="uploadModal" title="Загрузка фотографий">
                    <multiple-file-uploader id="fileUploader" postURL="/api/photos/" successMessagePath="" errorMessagePath=""></multiple-file-uploader>
                </b-modal>

              <b-dropdown right text="Пользователь" class="m-md-2" style="margin: 0px !important; margin-left: 5px; margin-right: 5px">
                <b-dropdown-item href="#">Профиль</b-dropdown-item>
                <b-dropdown-item v-on:click="logout()">Выйти</b-dropdown-item>
              </b-dropdown>
            </b-navbar-nav>

          </b-collapse>
        </b-navbar>
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