<template>
    <img id="imageItem" v-bind:src="'http://photoclo.ru:8000' + imageURL" alt=""/>
</template>

<script>

	export default {
		name: 'imageItem',
		props: ['imageURL'],
		methods: {}
	}
</script>

<style scoped>
    #imageItem {
    	border: 0px solid black;
        margin: 5px;
        margin-top: 10px;
        margin-bottom: 10px;
    }

    #imageItem:hover {
    	opacity: 0.8;
    	cursor: pointer;
    }
</style>
