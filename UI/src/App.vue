
<template>

    <div id="app">
        <!--<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">-->

        <b-navbar class="navBar" style="height: 50px" v-if="authenticated" toggleable="md" type="light" variant="light">

            <b-navbar-toggle target="nav_collapse"></b-navbar-toggle>

            <b-navbar-brand style="color: black; font-family: 'Lucida Console', serif; font-size: 30px !important;" href="photoclo.ru:8000">PHOTOCLO</b-navbar-brand>

            <b-collapse is-nav id="nav_collapse">



                <!-- Right aligned nav items -->
                <b-navbar-nav class="ml-auto">


                    <!--     Search     -->
                    <!--<form class="form-inline md-form form-sm mt-0">-->
                    <!--<i class="fas fa-search" aria-hidden="true"></i>-->
                    <!--<input class="form-control form-control ml-3 w-75" type="text" placeholder="Поиск" aria-label="Search">-->
                    <!--</form>-->

                    <div v-on:click="startUpload" class="iconDiv">
                        <div><img src="https://i.ibb.co/vJs3zrs/icon.png"  class="iconImg"/></div>
                        <span class="iconText">Загрузка</span>
                    </div>

                    <!--<span> myUploader.data().toClose </span>-->
                    <b-modal id="uploadModal" ref="uploadModal" hide-footer=true @hide="isModalShown=false" title="Загрузка фотографий">
                        <myUploader ref="myUploader" v-on:closeModal="isModalShown = false;" url="http://photoclo.ru:8000/api/photos/" @upload-image-success='updateImages();' @upload-image-failure='updateImages();'> </myUploader>
                    </b-modal>


                    <div class="iconDiv">
                        <div><img src="https://i.ibb.co/0cmbT5w/ya-disk.png" class="iconImg"></div>
                        <span class="iconText"> Яндекс.Диск </span>
                    </div>

                    <b-dropdown right text=""  class="mr-sm-2" id="dropUser" variant="link" no-caret>
                        <b-dropdown-item href="#">Профиль</b-dropdown-item>
                        <b-dropdown-item v-on:click="logout()">Выйти</b-dropdown-item>
                    </b-dropdown>

                    <!--<div class="iconDiv" id="userDiv">-->
                    <!--<img src="https://i.ibb.co/SDTzj5R/user-icon.png" class="iconImg" id="userImg"/>-->
                    <!--<b-dropdown id="userButton" right text=""  class="mr-sm-2" no-caret variant="link">-->
                    <!--<b-dropdown-item href="#">Профиль</b-dropdown-item>-->
                    <!--<b-dropdown-item v-on:click="logout()">Выйти</b-dropdown-item>-->
                    <!--</b-dropdown>-->
                    <!--</div>-->
                </b-navbar-nav>

            </b-collapse>
        </b-navbar>
        <router-view @authenticated="setAuthenticated" ref="child" />
    </div>
</template>

<script>
    import axios from 'axios';
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
                isModalShown: false,
            }
        },
        components: {
            myUploader
        },
        watch: {
            isModalShown(value) {
                console.log("I am in watcher")
                if (value) {
                    this.$refs.uploadModal.show();
                }
                else {
                    this.$refs.uploadModal.hide();
                }
            }
        },
        mounted() {

            if (localStorage.hasOwnProperty('token')) {
                this.token = localStorage.token;
                this.authenticated = true;
            }
            console.log(this.authenticated);
            if(!this.authenticated) {
                console.log("lol");
                this.$router.replace({ name: "login" });
            }
            else {
                console.log("kek");
                this.$router.replace({name: "secure"});
            }
        },

        methods: {
            updateToken () {
                document.getElementsByClassName('myUploadBox')[0].__vue__.$props.my_header = {Authorization: "Token " + localStorage.token};
            },
            setAuthenticated(status) {
                this.authenticated = status;
            },
            logout() {
                var this_ = this;
                axios.post('http://photoclo.ru:8000/api/sign_out/', {Authorization: "Token " + String(this.token)}).then(function () {
                    this_.authenticated = false;
                    this_.$router.replace({ name: "login" });
                    delete localStorage.token;
                });
            },
            updateImages() {
                this.$refs.child.updateImages();
            },
            resetUploader() {
                this.$refs.myUploader.resetUploader();
            },
            startUpload() {
                console.log("Start upload")
                this.isModalShown=true;
                this.updateToken();
                this.resetUploader()
            }
        },
    }
</script>

<style>
    body {
        background-color: #CCC !important;
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
        height: 100px;
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
    .navBar {
        height: 55px;
        background-color: #F8F8F8;
        border-color: #E7E7E7;
        border-bottom: 2px solid lightskyblue;

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
    #userImg {
        padding-bottom: 8px;
        height: 45px;
        width: auto;
    }
    .iconDiv {
        /*border: 1px solid grey;*/
        padding-top: 5px;
        padding-left: 5px;
        padding-right: 5px;
        padding-bottom: 2px;
        cursor: pointer;
        margin-top: 10px;
        margin-bottom: 10px;
        margin-left: 20px;
        margin-right: 25px;
        display: flex;
        flex-direction: row;
        text-align: center;
    }
    .iconDiv:hover {
        background-color: rgba(58, 120, 222, 0.05) !important;
    }
    .iconText {
        font-weight: 100;
        font-family: 'Lucida Console', serif;
        font-size: 17px;
        margin-left: 10px;
        margin-right: 10px;
    }
    .iconImg {
        width: 20px;
        height: 15px;
        margin-left: 10px;
    }
    #userButton {
        height: auto;
        background-color: red;
        color: red;
        margin-top: 0px;
    }
    #userImg {
        width: 30px;
        height: 35px;
        margin-bottom: 0px;
    }
    #uploadModal {
        font-family: 'Lucida Console', serif;
    }
    #dropUser {
        margin-left: 20px;
        margin-top: 14px;
        /*border: 1px solid black;*/
        padding-top: 10px;
        margin-right: 20px !important;
        /*background-image:url('http://www.w3.org/html/logo/downloads/HTML5_Logo_32.png');*/
        background-repeat:no-repeat;
        opacity: 1;
        width: 35px;
        height: 35px;
        background-image: url("https://i.ibb.co/sRkCGT4/Webp-net-resizeimage-7.png");
    }
    /*#userDiv {*/
    /*display: flex;*/
    /*flex-direction: column;*/
    /*}*/
</style>
