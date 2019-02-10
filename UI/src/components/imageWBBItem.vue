<template>
    <div id="id1">
    	<div class="myContainer">
        	<img id="image-WBB-Item" v-bind:src="'http://photoclo.ru:8000' + image.url" alt="" />
            <bbButton class="btn" v-for="(face, index) in faces" v-bind:key="'faceInput' + face.id" v-bind:face="face" v-bind:srcHeight="image.height" v-bind:srcWidth="image.width" v-bind:avatar="avatars[face.avatar]"/>
        </div>
    </div>
</template>

<script> 
    import bbButton from './bbButton.vue';
    

	export default {
		name: 'imageWBBItem',
        components: {
            bbButton
        },
        mounted: function() {
        },
		props: {
            image: {
                type: Object,
                default () {
                    return {};
                }
            },
            faces: {
                type: Array,
                default() {
                    return [];
                }
            },
            avatars: {
                type: Object,
                default() {
                    return {};
                }
            },
        },
        methods: {}
	}
</script>

<style scoped>
    #image-WBB-Item {
        width: auto;
        height: auto;
        max-height: 90vh;
        max-width: 90vw;
    }

    #id1 {
        display: flex;
        flex-direction: column;
        justify-content: space-around;
        width: 100%;
        height: 100%;
    }

    .myContainer {
        position: relative;
        width: 100%;
        height: auto;
    }

    /* Make the image responsive */
    .myContainer img {
        width: 100%;
        max-width: 100%;
        max-height: 100%;
    }

    /* Style the button and place it in the middle of the container/image */
    .myContainer .btn {
        position: absolute;
        transform: translate(-50%, -50%);
        -ms-transform: translate(-50%, -50%);
        border: none;
        cursor: pointer;
        border-radius: 5px;
    }
</style>