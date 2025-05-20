#include <iostream>
#include <vector>
#include <algorithm> // For std::max, std::min
#include <limits>    // For std::numeric_limits
class Project {
private:
    struct Task {
        int id;
        int duration;
        std::vector<int> predecessors_ids; // IDs of tasks that must be completed before this one
        std::vector<int> successors_ids;   // IDs of tasks that can start after this one is completed
        int est; // Earliest Start Time
        int eft; // Earliest Finish Time
        int lst; // Latest Start Time
        int lft; // Latest Finish Time
        int slack; // Allowed delay (LFT - EFT or LST - EST)
        Task(int _id = -1, int _duration = 0) :
            id(_id), duration(_duration),
            est(0), eft(0), lst(0), lft(0), slack(0) {}
    };

    int num_tasks;                      // Total number of tasks
    std::vector<Task> tasks_data;       // Stores all task objects
    int overall_project_completion_time; // Minimum time to complete the entire project

public:
    Project(int n) : num_tasks(n), overall_project_completion_time(0) {
        tasks_data.resize(n);
        for(int i = 0; i < n; ++i) {
            tasks_data[i].id = i; // Assign ID to each task based on its index
        }
    }

    void add_task_details(int task_id, int dur, const std::vector<int>& predecessors) {
        tasks_data[task_id].duration = dur;
        tasks_data[task_id].predecessors_ids = predecessors;
        // Build the successor list for each predecessor
        for (int pred_id : predecessors) {
            tasks_data[pred_id].successors_ids.push_back(task_id);
        }
    }

    void calculate_critical_path() {
        overall_project_completion_time = 0;
        for (int i = 0; i < num_tasks; ++i) {
            tasks_data[i].est = 0; // Initialize EST for the current task
            for (int pred_id : tasks_data[i].predecessors_ids) {
                tasks_data[i].est = std::max(tasks_data[i].est, tasks_data[pred_id].eft);
            }
            tasks_data[i].eft = tasks_data[i].est + tasks_data[i].duration;
            overall_project_completion_time = std::max(overall_project_completion_time, tasks_data[i].eft);
        }

        for (int i = 0; i < num_tasks; ++i) {
            tasks_data[i].lft = overall_project_completion_time;
        }
        for (int i = num_tasks - 1; i >= 0; --i) {
            if (tasks_data[i].successors_ids.empty()) {

            } else {
                // For tasks with successors, LFT is the minimum LST of all its successors.
                int min_successor_lst = std::numeric_limits<int>::max();
                for (int succ_id : tasks_data[i].successors_ids) {
                    min_successor_lst = std::min(min_successor_lst, tasks_data[succ_id].lst);
                }
                tasks_data[i].lft = min_successor_lst;
            }
            tasks_data[i].lst = tasks_data[i].lft - tasks_data[i].duration;
        }

        for (int i = 0; i < num_tasks; ++i) {
            tasks_data[i].slack = tasks_data[i].lft - tasks_data[i].eft;
        }
    }

    int get_project_completion_time() const {
        return overall_project_completion_time;
    }

    std::vector<int> get_slack_times() const {
        std::vector<int> slacks(num_tasks);
        for (int i = 0; i < num_tasks; ++i) {
            slacks[i] = tasks_data[i].slack;
        }
        return slacks;
    }
};

int main() {
    std::ios_base::sync_with_stdio(false);
    std::cin.tie(NULL);

    int n; // Number of tasks
    std::cin >> n;

    Project project(n); // Create a Project object
    for (int i = 0; i < n; ++i) {
        int task_id_from_input; // Task ID from input (guaranteed to be i)
        int duration;
        int num_predecessors;
        std::cin >> task_id_from_input >> duration >> num_predecessors;

        std::vector<int> predecessors(num_predecessors);
        for (int j = 0; j < num_predecessors; ++j) {
            std::cin >> predecessors[j];
        }
        project.add_task_details(i, duration, predecessors);
    }

    project.calculate_critical_path();

    std::cout << project.get_project_completion_time() << std::endl;
    std::vector<int> slacks = project.get_slack_times();
    for (int i = 0; i < n; ++i) {
        std::cout << slacks[i] << std::endl;
    }

    return 0;
}
