import { spawn } from "child_process";

export default function spawn_llm(cmd, ip, port, text) {
  const child = spawn("python", [cmd, ip, port, text], {
    stdio: "inherit", // inherit stdio so you can see output in parent console
  });

  // cleanup function to kill child when parent exits
  function cleanup() {
    if (!child.killed) {
      child.kill();
    }
  }

  // listen for parent exit events to clean up child process
  process.on("exit", cleanup);
  process.on("SIGINT", () => {
    cleanup();
    process.exit();
  });
  process.on("SIGTERM", () => {
    cleanup();
    process.exit();
  });

  // parent continues running separately
  console.log("Parent app running, child process spawned");
}
