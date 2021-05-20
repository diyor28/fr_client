<template>
    <v-content>
    </v-content>
</template>

<script>
    export default {
        name: "Home",
        mounted: function () {
                this.$router.push({path: '/cameras'})
        },
    }
</script>

<style scoped>

</style>