<template>
    <div class="dropdown mybbButton" v-bind:style="getStyle()">
        <input type="text" v-bind:id="'faceInput' + face.id" class="nameInput" placeholder="Кто это?" required v-on:change="updateName" v-on:keyup.enter="inputSubmit()"  />
    </div>
</template>

<script>
    import axios from 'axios';

    var pixelWidth = require('string-pixel-width');

    function resizable (el, factor) {
        var int = Number(factor) || 7.7;
        function resize() {
            el.style.width = String(Math.max(100, pixelWidth(el.value, {size: 20}) + 10)) + 'px';
        }
        var e = 'keyup,keypress,focus,blur,change'.split(',');
        for (var i in e) el.addEventListener(e[i],resize,false);
            resize();
    }

	export default {
		name: 'bbButton',
		props: ['srcWidth', 'srcHeight', 'face', 'avatar'],
        data() {
            return {
                name: ''
            };
        },
        watch: {},
        mounted: function () {
            resizable(document.getElementById('faceInput' + String(this.face.id)), 13);
            if (this.face.user_checked) {
                var inp = document.getElementById('faceInput' + this.face.id);
                console.log(this.avatar);
                inp.value = this.avatar.name;
                inp.disabled = true;
                inp.style.width = String(pixelWidth(inp.value, {size: 20}) + 10) + 'px';
                inp.style.color = "#CCC !important";
                inp.style.backgroundColor = "rgba(0, 0, 0, 0.5) !important";
            }
        },
		methods: {
            getStyle() {
                var x1 = this.face.bounding_box[0];
                var y1 = this.face.bounding_box[1];
                var x2 = this.face.bounding_box[2];
                var y2 = this.face.bounding_box[3];
                var height = y2 - y1;
                var width = x2 - x1;
                var st = '';
                st = st + 'height: ' + String(height * 100 / this.srcHeight) + '%;';
                st = st + 'width: ' + String(width * 100 / this.srcWidth) + '%;';
                st = st + 'left: ' + String((x1 + x2) * 50 / this.srcWidth) + '%;';
                st = st + 'top: ' + String((y1 + y2) * 50 / this.srcHeight) + '%;';
                return st;
            },
            updateName(event) {
                this.name = event.target.value;
            },
            inputSubmit() {
                var inp = document.getElementById('faceInput' + this.face.id);
                inp.disabled = true;
                var this_ = this;
                axios({ method: 'PATCH', url: '/api/avatars/' + this_.face.avatar + '/', headers: { Authorization: "Token " + localStorage.token}, data: {'new_name': this_.name, 'face': this_.face.id }}).then(function(response) {
                }).catch(function (error) {
                    console.log(error);
                });
            }
        },
	}
</script>

<style scoped>

    .dropdown {
        position: relative;
        background-color: rgba(0, 0, 0, 0) !important;
        margin: 0px !important;
        padding: 0px !important;
        border: 2px solid rgba(255, 255, 0, 0.5) !important;
        display: flex;
        flex-direction: column;
        align-items: center;
    }

    .mybbButton:hover {
        border: 3px solid rgba(255, 255, 0, 1) !important;
        margin-bottom: 3px !important;
    }

    .nameInput {
        position: absolute;
        align-self: center;
        display: none;
        font-size: 20px;
        height: auto;
        top: 100%;
        border: 2px solid white;
        border-radius: 2px;
        width: 100px;
        transition: width 0.05s;
        text-align: center;
    }

    .dropdown:hover .nameInput {
        display: block;
    }
</style>