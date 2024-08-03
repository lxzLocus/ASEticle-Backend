import matching
import time

if __name__ == '__main__':
    entries = [
        {"conference": ""},
        {"conference": "ICSE"},
        {"conference": "ICSE"},
        {"conference": "IEEE International Conference on Pervasive Computing and Communications"},
        {"conference": "IEEE International Conference on Pervasive"},
        {"conference": "International Conference on Multimodal Interaction"},
        {"conference": "hoge zxqjb"},
        {"conference": "ACM"},
        {"conference": ""},
        {"conference": "International Visualization in Transportation Symposium"}
    ]
    
    # start = time.perf_counter()
    # print(matching.entries_match(entries))
    # end = time.perf_counter()
    # print(f"OneShotMode Time: {end - start} s")
    
    # start = time.perf_counter()
    # print(matching.eager_match_conferences(entries))
    # end = time.perf_counter()
    # print(f"EagerMode Time: {end - start} s")
    
    start = time.perf_counter()
    print(matching.match_conferences(entries))
    end = time.perf_counter()
    print(f"MainMode Time: {end - start} s")