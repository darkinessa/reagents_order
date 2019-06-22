    $(document).ready(function () {
        $(function () {
            $('body').on('click', '.modal-link', function (e) {
                e.preventDefault();
                $(this).attr('data-target', '#modal-container');
                $(this).attr('data-toggle', 'modal');
            });

            $('body').on('click', '.modal-close-btn', function () {
                $('#modal-container').modal('hide');
            });
            $('#modal-container').on('hidden.bs.modal', function () {
                $(this).removeData('bs.modal');
            });

            $('#CancelModal').on('click', function () {
                return false;
            });
        });
        });

                              <!-- Button trigger modal -->
          <button type="button" class="btn btn-warning" data-toggle="modal" data-target="#exampleModalCenter{{item.id}}">
              <span class="glyphicon glyphicon-trash"></span>
          </button>
          <!-- Modal -->
          <div class="modal fade" id="exampleModalCenter{{item.id}}">
            <div class="modal-dialog modal-dialog-centered" role="document">
              <div class="modal-content">
                <div class="modal-header">
                  <h5 class="modal-title" id="exampleModalLongTitle{{item.id}}">Вы хотите удалить реагент?</h5>
                  <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                    <span aria-hidden="true">&times;</span>
                  </button>
                </div>
                <div class="modal-body">
                  <h3>{{item.reagent_name}}</h3>
                  <p>Подтвердите удаление</p>
                </div>
                <div class="modal-footer">
                     <form action="{{url_for('del_draft_item', id=item.id)}}" method="post">
                    <input type="submit" value="Удалить" class="btn btn-primary">
                  </form>

                  <button type="button" class="btn btn-secondary" data-dismiss="modal">Отменить</button>