<template>
  <q-page class="flex flex-center justify-center">
    <div class="example-row-horizontal-alignment">
      <div class="q-pb-xl row justify-around items-center">

        <div class="row items-center q-pa-md justify-left col-4">
          <div class="text-h2 text-weight-bold">
            <p>Your Money, Your Control</p>
          </div>
          
          <div>
            <p>Making peer-to-peer electronic cash accessible to everyone, everywhere.</p>
          </div>

          <div>
            <q-btn no-wrap 
            class="justify-left text-capitalize" 
            outline rounded 
            color="accent" 
            icon-right="start" 
            label="Register to our payment gateway"
            @click="$router.push('register')" />
          </div>

        </div>

        <div class="row items-center q-pa-md col-4">
            <img src="src/assets/images/home_pic.png" alt="Photo">
        </div>
      </div>
    </div>
  </q-page>
</template>

<style>
.home {
  background-image: url(/src/assets/images/home_pic.png);
  background-size: cover;
}
</style>