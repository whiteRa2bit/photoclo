<template>

    <div id="app">
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">

        <b-navbar v-if="authenticated" toggleable="md" type="dark" variant="info">

            <b-navbar-toggle target="nav_collapse"></b-navbar-toggle>

            <b-navbar-brand href="photoclo.ru:8000">PHOTOCLO</b-navbar-brand>

            <b-collapse is-nav id="nav_collapse">



                <!-- Right aligned nav items -->
                <b-navbar-nav class="ml-auto">

                    <form class="form-inline md-form form-sm mt-0">
                        <i class="fas fa-search" aria-hidden="true"></i>
                        <input class="form-control form-control ml-3 w-75" type="text" placeholder="Поиск" aria-label="Search">
                    </form>


                    <b-button v-b-modal.uploadModal class="mr-sm-2" v-on:click="updateToken(); updateModalShown" right>Загрузить</b-button>
                    <!--<span> myUploader.data().toClose </span>-->
                    <b-modal v-if="isModalShown" id="uploadModal" ref="uploadModal" hide-footer=true @hide="canselUploader" title="Загрузка фотографий">
                        <myUploader ref="myUploader" v-on:closeModal="updateModalShown" url="http://photoclo.ru:8000/api/photos/" @upload-image-success='updateImages' @upload-image-failure='updateImages'> </myUploader>
                        <!--
                        <multiple-file-uploader id="fileUploader" postURL="/api/photos/" successMessagePath="" errorMessagePath="" @upload-success='updateImages' @upload-error='updateImages'></multiple-file-uploader>
                        --->
                    </b-modal>
                    <b-dropdown right text="Пользователь"  class="mr-sm-2">
                        <b-dropdown-item href="#">Профиль</b-dropdown-item>
                        <b-dropdown-item v-on:click="logout()">Выйти</b-dropdown-item>
                    </b-dropdown>
                </b-navbar-nav>

            </b-collapse>
        </b-navbar>
        <router-view @authenticated="setAuthenticated" ref="child" />
    </div>
</template>

<script>
    import axios from 'axios';
    import MultipleFileUploader from './components/MultipleFileUploader.vue';
    import myUploader from './components/myUploader.vue'
    var modal = document.getElementById('id01');

    window.onclick = function(event) {
        if (event.target == modal) {
            modal.style.display = "none";
        }
    }

    window.onload = function() {
        var this_ = this;
        document.getElementsByClassName('myUploader')[0].__vue__.$props.my_header = {Authorization: "Token " + localStorage.token};
    }

    export default {
        name: 'App',
        data() {
            return {
                authenticated: false,
                token: undefined,
                isModalShown: false
            }
        },
        components: {
            MultipleFileUploader,
            myUploader
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
                this.isModalShown = true;
                console.log(localStorage.token);
                document.getElementsByClassName('myUploadBox')[0].__vue__.$props.my_header = {Authorization: "Token " + localStorage.token};
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
            },
            updateImages() {
                this.$refs.child.updateImages();
            },
            updateModalShown: function () {
                console.log("inside updateModalShown")
                this.isModalShown = !this.isModalShown;
            },
            canselUploader() {
                console.log("inside canselUploader")
                this.$refs.uploadModal.html = "";
                this.$refs.myUploader.resetUploader();
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
