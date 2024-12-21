import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


def read_input_file(filename):
    """Чтение входного файла и извлечение переменных."""
    variables = {}
    with open(filename, "r") as file:
        for line in file:
            key, value = line.strip().split("=", 1)
            key = key.strip()
            value = eval(value.strip())
            variables[key] = value
    return variables


def write_results_to_file(filepath, results):
    """Запись результатов в файл."""
    with open(filepath, "w") as file:
        for key, values in results.items():
            print(f"{key}={values}", file=file)


def generate_latex_table_rows_pipes(pipes):
    """Генерация строки для LaTeX с номерами труб."""
    return "& " + " & ".join(f"\\texttt{{{value}}}" for value in pipes) + " \\\\"


def generate_latex_table_rows_results(keys, arrays, start=0, end=None):
    """Генерация строк для LaTeX с результатами."""
    rows = []
    for key, values in zip(keys, arrays):
        selected_values = values[start:end]
        formatted_values = " & ".join(f"${value:.2f}$" for value in selected_values)
        rows.append(f"\\texttt{{{key}}} & {formatted_values} \\\\")
    return rows


def plot_3d_surface(pipes, macros, all_results, lim, save_path, filename):
    """Построение 3D-графика."""
    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot(111, projection="3d")

    X, Y = np.meshgrid(pipes, range(len(macros)))
    Z = np.array([result for result in all_results])

    surf = ax.plot_surface(X, Y, Z, cmap="inferno", edgecolor="none")

    ax.set_xlabel("Pipes", fontsize=15, labelpad=12)
    ax.set_ylabel("Macros", fontsize=15, labelpad=25)
    ax.set_zlabel("Time", fontsize=15, labelpad=15)
    ax.tick_params(axis="x", labelsize=13)
    ax.tick_params(axis="y", pad=9, labelsize=13)
    ax.tick_params(axis="z", labelsize=13)
    ax.set_zlim([0, lim])
    ax.set_yticks(range(len(macros)))
    ax.set_yticklabels(macros)

    fig.colorbar(surf, ax=ax, pad=0.15, shrink=0.6)
    fig.canvas.manager.set_window_title(filename)

    plt.savefig(save_path + filename, dpi=300, format="pdf")
    plt.show()
    plt.close(fig)


def plot_line_graph(pipes, macros, all_results, lim, save_path, filename):
    """Построение линейного графика."""
    fig, ax = plt.subplots(figsize=(12, 8))
    macros_indices = range(len(macros))

    for i, pipe in enumerate(pipes):
        line_data = [all_results[j][i] for j in range(len(all_results))]
        ax.plot(macros_indices, line_data, marker="o", label=f"Pipe: {pipe}")

    ax.set_xticks(macros_indices)
    ax.set_xticklabels(macros)
    ax.set_xlabel("Macros", fontsize=20)
    ax.set_ylabel("Time", fontsize=20)
    ax.tick_params(axis="x", labelsize=18)
    ax.tick_params(axis="y", labelsize=18)
    ax.set_ylim([-10, lim])
    ax.legend(fontsize=16.5)
    fig.canvas.manager.set_window_title(filename)

    plt.grid(True)
    plt.tight_layout()
    plt.savefig(save_path + filename, dpi=300, format="pdf")
    plt.show()
    plt.close(fig)


def print_latex_tables(pipes, macros, all_results):
    """Вывод строк для LaTeX-таблиц."""
    lines1 = generate_latex_table_rows_results(macros, all_results, 0, 9)
    lines2 = generate_latex_table_rows_results(macros, all_results, 9)

    print(generate_latex_table_rows_pipes(pipes[:9]))
    print("\\hline")
    for elem in lines1:
        print(elem)
    print("\\vspace{0.4cm} \\\\")
    print(generate_latex_table_rows_pipes(pipes[9:]))
    print("\\hline")
    for elem in lines2:
        print(elem)


if __name__ == "__main__":
    title = "mpi_o3"
    write_results = False
    # write_results = True

    save_path = "./graph/"
    read_path = "./results/"
    lim = 350 if title == "mpi" else 150

    if not write_results:
        data = read_input_file(read_path + title + ".txt")
        results_SMALL = data["results_SMALL"]
        results_MIDDLE = data["results_MIDDLE"]
        results_LARGE = data["results_LARGE"]
        results_EXTLARGE = data["results_EXTLARGE"]

    # results_SMALL=[0.110787, 0.067214, 0.063037, 0.058088, 0.083459, 0.081243, 0.051404, 0.060263, 0.05155, 0.071098, 0.032519, 0.04515, 0.065723, 0.091094, 0.136212, 0.120807, 0.646959, 0.496774]
    # results_MIDDLE=[0.931851, 0.497245, 0.437693, 0.540993, 0.566705, 0.669349, 0.566349, 0.337128, 0.358836, 0.304021, 0.142427, 0.198656, 0.292256, 0.376539, 0.624868, 0.428697, 0.941634, 0.677605]
    # results_LARGE=[25.026308, 15.443051, 11.758131, 7.866836, 5.077578, 3.150042, 3.039332, 2.587785, 2.005004, 2.034282, 1.736706, 1.951426, 2.051116, 4.1813, 4.062121, 4.145007, 4.909373, 5.309015]
    # results_EXTLARGE=[149.600611, 82.496043, 56.75903, 20.610923, 25.270447, 22.692715, 19.249695, 26.634133, 13.210994, 12.018836, 11.722738, 11.896462, 14.688057, 24.324574, 28.012847, 26.452516, 26.318955, 28.805096]

    pipes = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 20, 40, 60, 80, 100, 120, 140, 160]
    macros = ["SMALL", "MIDDLE", "LARGE", "EXTLARGE"]
    all_results = [results_SMALL, results_MIDDLE, results_LARGE, results_EXTLARGE]

    if write_results:
        write_results_to_file(
            read_path + title + ".txt",
            {
                "results_SMALL": results_SMALL,
                "results_MIDDLE": results_MIDDLE,
                "results_LARGE": results_LARGE,
                "results_EXTLARGE": results_EXTLARGE,
            },
        )

    print_latex_tables(pipes, macros, all_results)

    plot_3d_surface(pipes, macros, all_results, lim, save_path, f"{title}.pdf")
    plot_line_graph(pipes, macros, all_results, lim, save_path, f"{title}1.pdf")
