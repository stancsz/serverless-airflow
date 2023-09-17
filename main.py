import os
import logging
from datetime import datetime
import yaml
from flask import Flask, request, jsonify

app = Flask(__name__)

def main(request):
    log_buffer = []

    class BufferingHandler(logging.Handler):
        def emit(self, record):
            log_buffer.append(self.format(record))

    if not os.path.exists('logs'):
        os.makedirs('logs')

    log_filename = f'logs/run_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'
    logging.basicConfig(
        filename=log_filename,
        level=logging.DEBUG,
        format='[%(asctime)s] {%(filename)s:%(lineno)d} %(levelname)s - %(message)s'
    )

    logging.getLogger().addHandler(BufferingHandler())

    req_data = request.json

    # Load dag_code and config.yml from user's request
    dynamic_dag_code = req_data.get('dag_code', '')
    config_yml_str = req_data.get('config_yml', '')

    # Convert YAML string to dict
    dag_config = yaml.safe_load(config_yml_str)
    logging.info(f"Loaded DAG configuration: {dag_config}")

    exec_globals = {'logging': logging, 'dag_config': dag_config}

    # Execute dag_code
    exec(dynamic_dag_code, globals(), exec_globals)

    # Retrieve the DAG
    dag = exec_globals.get('dag')

    task_status = {}
    if dag:
        context = {}
        for task_id, task in dag.task_dict.items():
            upstream_succeeded = all(
                task_status.get(upstream_task_id, False)
                for upstream_task_id in task.upstream_task_ids
            )

            if upstream_succeeded:
                logging.info(f"Executing task: {task_id}")
                task.execute(context=context)
                task_status[task_id] = True
            else:
                logging.info(f"Skipping task: {task_id} as upstream tasks have not succeeded.")
                task_status[task_id] = False
    else:
        logging.info("Couldn't find DAG.")

    log_output = '\n'.join(log_buffer)
    return jsonify({'logs': log_output})

@app.route('/', methods=['POST'])
def index():
    return main(request)

if __name__ == "__main__":
    sample_dag_code = ''''''
    sample_config_yml = ''''''

    with app.test_client() as c:
        response = c.post('/', json={
            'dag_code': sample_dag_code,
            'config_yml': sample_config_yml
        })
        print(response.get_json())
