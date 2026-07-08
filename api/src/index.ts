import { Hono } from "hono";
import { cors } from "hono/cors";

const app = new Hono<{Bindings: CloudflareBindings}>()

app.use(
  cors({
    origin: "*", // customize this to only allow certain domains!
  }),
);

app.get("/", (c) => {
  return c.text("Hello Hono!");
});

export default app;
