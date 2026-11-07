"""C/C++ build before a mutant is tested: the commands run without a shell."""

import sys


def test_command(directory):
    if (directory / 'CMakeLists.txt').is_file():
        build = 'target/cpp-mutation-build'
        commands = [
            ['cmake', '-S', '.', '-B', build, '-DBUILD_TESTING=ON', '-DCMAKE_BUILD_TYPE=Debug'],
            ['cmake', '--build', build, '--config', 'Debug', '--clean-first'],
            ['ctest', '--test-dir', build, '-C', 'Debug', '--output-on-failure', '--no-tests=error'],
        ]
        script = 'import subprocess\nfor command in ' + repr(commands) + ':\n    subprocess.run(command, check=True)\n'
        return [sys.executable, '-c', script]
    if (directory / 'Makefile').is_file() or (directory / 'makefile').is_file():
        return ['make', '-B', 'test']
    print('C/C++ needs a CMakeLists.txt, a Makefile, or an explicit --test-command.', file=sys.stderr)
    return ['false']
