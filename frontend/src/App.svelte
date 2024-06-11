<script>
  import { Router, Route, useLocation } from "svelte-routing";
  import Header from "./components/Header.svelte";
  import Home from "./routes/Home.svelte";
  import Workspace from "./routes/Workspace.svelte";
  import About from "./routes/About.svelte";
  import Login from "./routes/Login.svelte";
  import Authorize from "./routes/Authorize.svelte";

  import Test from "./routes/WorkspaceTest.svelte";

  export let url = "";
  const location = useLocation();

  import { validate_token } from "./api/auth";

  // Вызываем функцию проверки токена при загрузке компонента
  // Например, в onMount
  import { onMount } from "svelte";
  onMount(() => {
    validate_token();
  });
</script>

<Router {url}>
  <!-- <nav>
    <Link to="/">Home</Link>
    <Link to="/workspace">Workspace</Link>
    <Link to="/about">About</Link>
    <Link to="/login">Login</Link>
    <Link to="/registration">Registration</Link>
  </nav> -->
  <div>
    <Route component={Home} />
    <Route path="/workspace" component={Workspace} />
    <Route path="/about" component={About} />
    <Route path="/login" component={Login} />
    <Route path="/authorize" component={Authorize} />

    <Route path="/test" component={Test} />
  </div>
</Router>
