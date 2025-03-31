<template>
<div class="container text-center">
    <div class="row">
        <div class="col">
            <div class="card">
                <div class="card-header">
                    Customer
                </div>
                <div class="card-body">
                    <p class="card-text">With supporting text below as a natural lead-in to additional content.</p>
                    <a href="/login?type=CL" class="btn btn-primary m-2">Login</a>
                    <a href="/signup/customer" class="btn btn-info m-2">Register</a>

                </div>
            </div>
        </div>
        <div class="col">
            <div class="card">
                <div class="card-header">
                    Professional 
                </div>
                <div class="card-body">
                    <p class="card-text">With supporting text below as a natural lead-in to additional content.</p>
                    <a href="/login?type=PL" class="btn btn-primary m-2">Login</a>
                    <a href="/signup/professional" class="btn btn-info m-2">Register</a>
                </div>
            </div>
        </div>
        <div class="col">
            <div class="card">
                <div class="card-header">
                    Admin 
                </div>
                <div class="card-body">
                    <p class="card-text">With supporting text below as a natural lead-in to additional content.</p>
                    <a href="/login?type=AL" class="btn btn-primary m-2">Login</a>
                    <a href="mailto: admin@email.com" class="btn btn-info m-2">Contact</a>

                </div>
            </div>
        </div>
    </div>
</div>
</template>

<script>
// @ is an alias to /src

export default {
  name: 'HomeView',
  // components: {
  //   HelloWorld
  // }
}
</script>
