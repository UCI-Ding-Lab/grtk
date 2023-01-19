def preference(options: dict):
    if options["style"] == "solid+dot":
        parameters = dict(
            markersize=options["dot_size"],
            marker="o",
            markerfacecolor=options["dot_color"],
            markeredgecolor=options["dot_color"],
            linestyle="solid",
            linewidth=options["width"],
            fillstyle="full",
            color=options["line_color"],
        )
    elif options["style"] == "dot":
        parameters = dict(
            markersize=options["dot_size"],
            marker="o",
            markerfacecolor=options["dot_color"],
            markeredgecolor=options["dot_color"],
            linestyle="None",
        )
    else:
        parameters = dict(
            linewidth=options["width"],
            linestyle=options["style"],
            color=options["line_color"],
        )
    return parameters