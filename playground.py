from source import parser


def parser_test() -> None:
    parser_object = parser.Parser()
    result = parser_object.parse_map(
        "/Users/ceren/Desktop/Codam/Milestone_03/fly_in/maps/easy/"
        "01_linear_path.txt",
    )
    drone_count, graph_instance = result
    print(result)


parser_test()
