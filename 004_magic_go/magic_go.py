import pygame
import sudokum

class Button:  
    def __init__(self, x, y, width, height, text, color=(255, 255, 255)):  
        self.rect = pygame.Rect(x, y, width, height)  
        self.color = color  
        self.text = text  
        self.font = pygame.font.Font(None, 16)  
        self.text_surface = self.font.render(self.text, True, (0, 0, 0))  
  
    def draw(self, screen):  
        pygame.draw.rect(screen, self.color, self.rect)  
        screen.blit(self.text_surface, (self.rect.left + (self.rect.width - self.text_surface.get_width()) // 2,  
                                        self.rect.top + (self.rect.height - self.text_surface.get_height()) // 2))  
  
    def is_clicked(self, event):  
        if event.type == pygame.MOUSEBUTTONDOWN:  
            mouse_pos = event.pos  
            if self.rect.collidepoint(mouse_pos):  
                return True  
        return False
    
class Cell:
    def __init__(self, x=None, y=None, text=None, cell_type=0):
        """
        cell_type:
        0: 未选中, 已填入
        1: 未选中, 草稿
        2: 已选中, 已填入
        3: 联动,   草稿
        """
        self.lock = 0
        self.x = x
        self.y = y
        self.cell_type = cell_type
        self.text = text

    def __init(self):
        if self.cell_type == 0:
            self.text_color = 'DarkGreen'
            self.cell_color = 'Wheat'
            self.text_size = 30
            self.wh = 60
        elif self.cell_type == 1:
            self.text_color = 'SlateGray'
            self.cell_color = 'Wheat'
            self.text_size = 15
            self.wh = 60
        elif self.cell_type == 2:
            self.text_color = 'Wheat'
            self.cell_color = 'DarkGreen'
            self.text_size = 30
            self.wh = 60
        elif self.cell_type == 3:
            self.text_color = 'Wheat'
            self.cell_color = 'SlateGray'
            self.text_size = 15
            self.wh = 60
        else:
            raise Exception("无效单元格类型")

    def draw(self, screen):
        self.__init()
        self.rect = pygame.Rect(self.x, self.y, self.wh, self.wh)
        self.font = pygame.font.SysFont("Arial", self.text_size)

        if self.lock == 1:
            self.cell_color = 'LightYellow'
        elif self.lock == 2:
            self.cell_color = 'LawnGreen'
        elif self.lock == 3:
            self.cell_color = 'Green'
        else:
            pass
        pygame.draw.rect(screen, self.cell_color, self.rect)

        if len(self.text) == 1:
            text_surface = self.font.render(self.text[0], True, self.text_color)
            screen.blit(text_surface, (self.x + 22, self.y + 16))
        else:
            row_h = 0
            for t in self.text:
                text_surface = self.font.render(t, True, self.text_color)
                screen.blit(text_surface, (self.x, self.y + row_h))
                row_h += 20

    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            if self.rect.collidepoint(mouse_pos):
                return True
        return False


def shoot(bd, ii, jj, value):
    """
    从每行列块草稿里清除已确定的值
    每次调用只做一个步骤
    """
    for n in range(1, 10):
        # 行
        vr = bd[str(ii) + str(n)]
        if len(vr) > 1 and value in vr:
            bd[str(ii) + str(n)] = [x for x in vr if x != value]
            return 'clear value:[ %s ] in cell(%s, %s)' % (str(value), str(ii), str(n)), ii, n
        # 列
        vc = bd[str(n) + str(jj)]
        if len(vc) > 1 and value in vc:
            bd[str(n) + str(jj)] = [x for x in vc if x != value]
            return 'clear value:[ %s ] in cell(%s, %s)' % (str(value), str(n), str(jj)), n, jj
    # 块
    for bi in range(int(ii / 3.5) * 3 + 1, int(ii / 3.5) * 3 + 4):
        for bj in range(int(jj / 3.5) * 3 + 1, int(jj / 3.5) * 3 + 4):
            vb = bd[str(bi) + str(bj)]
            if len(vb) > 1 and value in vb:
                bd[str(bi) + str(bj)] = [x for x in vb if x != value]
                return 'clear value:[ %s ] in cell(%s, %s)' % (str(value), str(bi), str(bj)), bi, bj
    return 'Done', 0, 0


def search(bd):
    """
    从每行列块草稿里找到只出现一次的值, 更新为确定值
    每次调用只做一个步骤
    """
    for n in range(1, 10):
        # 行
        cfm_v = []
        for ii in range(1, 10):  # 遍历cell
            bdv = bd[str(n) + str(ii)]
            if len(bdv) == 1:
                cfm_v.append(bdv[0])
        v_cnt = {}
        v_cnt_inx = {}
        for v in range(1, 10):
            if v in cfm_v: continue
            if v not in v_cnt.keys():
                v_cnt[v] = 0
                v_cnt_inx[v] = 0
            for ii in range(1, 10):
                bdv = bd[str(n) + str(ii)]
                if v in bdv:
                    v_cnt[v] += 1
                    v_cnt_inx[v] = ii
        for v in range(1, 10):
            if v in cfm_v: continue
            if v_cnt[v] == 1:
                bd[str(n) + str(v_cnt_inx[v])] = [v]
                return 'Rise value:[ %s ] in cell(%s, %s)' % (str(v), str(n), str(v_cnt_inx[v])), n, v_cnt_inx[v]
        # 列
        cfm_v = []
        for ii in range(1, 10):
            bdv = bd[str(ii) + str(n)]
            if len(bdv) == 1:
                cfm_v.append(bdv[0])
        v_cnt = {}
        v_cnt_inx = {}
        for v in range(1, 10):
            if v in cfm_v: continue
            if v not in v_cnt.keys():
                v_cnt[v] = 0
                v_cnt_inx[v] = 0
            for ii in range(1, 10):
                bdv = bd[str(ii) + str(n)]
                if v in bdv:
                    v_cnt[v] += 1
                    v_cnt_inx[v] = ii
        for v in range(1, 10):
            if v in cfm_v: continue
            if v_cnt[v] == 1:
                bd[str(v_cnt_inx[v]) + str(n)] = [v]
                return 'Rise value:[ %s ] in cell(%s, %s)' % (str(v), str(n), str(v_cnt_inx[v])), n, v_cnt_inx[v]

    # # 块
    # for bi in [1,4,7]:
    #     for bj in [1,4,7]:
    #         cfm_v = []
    #         for ii in range(bi,bi+3):
    #             for jj in range(bj,bj+3):
    #                 bdv = bd[str(ii)+str(jj)]
    #                 if len(bdv)==1:
    #                     cfm_v.append(bdv[0])
    #         for v in range(1,10):
    #             v_cnt = {}
    #             v_cnt_inx = {}
    #             for ii in range(bi,bi+3):
    #                 for jj in range(bj,bj+3):
    #                     if v in cfm_v: continue
    #                     if v not in v_cnt.keys():
    #                         v_cnt[v] = 0
    #                         v_cnt_inx[v]=''
    #             for ii in range(1,10):
    #                 bdv = bd[str(ii)+str(jj)]
    #                 if v in bdv:
    #                     v_cnt[v]+=1
    #                     v_cnt_inx[v] = str(ii)+str(jj)
    #         for v in range(1, 10):
    #             if v in cfm_v: continue
    #             if v_cnt[v] == 1:
    #                 bd[v_cnt_inx[v]] = [v]
    #                 return 'Rise value:[ %s ] in cell(%s, %s)' % (str(v), str(v_cnt_inx[v])[0], str(v_cnt_inx[v]))[1], str(v_cnt_inx[v])[0], str(v_cnt_inx[v])[1]

    return 'Done', 0, 0

def draft(bd):
    for i in range(1, 10):
        for j in range(1, 10):
            if input_sudo[i - 1][j - 1] == 0:
                bd[str(i) + str(j)] = [x for x in range(1, 10)]
            else:
                bd[str(i) + str(j)] = [input_sudo[i - 1][j - 1]]

def update(bd):
    global running
    if running is False:
        draft(bd)
        running = True
    for ii in range(1, 10):
        for jj in range(1, 10):
            values = bd[str(ii) + str(jj)]
            if len(values) == 1:
                shoot_msg, rn, cn = shoot(bd, ii, jj, values[0])
                if shoot_msg == 'Done':
                    continue
                data = [ii, jj, rn, cn]
                return shoot_msg, data

    search_msg, rn, cn = search(bd)
    if search_msg == 'Done':
        return 'Done', [0, 0, 0, 0]
    else:
        data = [0, 0, rn, cn]
        return search_msg, data



def finish(bd):
    if len(bd) == 0:
        return False
    std = {1,2,3,4,5,6,7,8,9}
    for n in range(1, 10):
        row = []
        for ii in range(1,10):
            row.append(bd[str(n)+str(ii)][0])
        row = set(row)
        if row != std:
            return False
        col = []
        for ii in range(1,10):
            col.append(bd[str(ii)+str(n)][0])
        col = set(col)
        if col != std:
            return False

    for ii in [1,4,7]:
        for jj in [1,4,7]:
            bc = {bd[str(iii)+str(jjj)][0] for iii in range(ii,ii+3) for jjj in range(jj,jj+3)} 
            if bc != std:
                return False
    return True
         

board = {}
running = False

pos = {
    'msg': (850, 50),
}

size = {
    'grid': 72,
    'grid_line': 5,
    'grid_line_light': 1,
    'grid_margin': 6,
    'cell_margin': 0,
    'cell_radius_cfm': 28,
    'cell_radius_draft': 13,
    'font_cfm': 23,
    'font_draft': 15
}

color = {
    'bg': 'Honeydew',
    'line': 'Black',
    'msg': 'Black',
}


screen_x = 1000
screen_y = 800

pygame.init()
screen = pygame.display.set_mode((screen_x, screen_y))
clock = pygame.time.Clock()
pygame.display.set_caption('MyShudoku')
button_go = Button(750, 50, 80, 50, 'Go', 'SteelBlue')
button_draft = Button(750, 110, 80, 50, 'AutoGo', 'SteelBlue')
button_new = Button(750, 170, 80, 50, 'New', 'SteelBlue')

button_num = {i: Button(60*i, 5, 50, 50, str(i), 'GoldEnrod') for i in range(1,10)}
button_num_cnt = {i:9 for i in range(1,10)}

count = 0
msg = ''
data = [0, 0, 0, 0]
msg_display = []
auto = False
todo = True

cell_matrix = {}


cur_cell = ''
rel_cells = []
rel_value_cells = []
while True:
    go = False
    down_k = None
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        elif pygame.mouse.get_pressed():
            if button_draft.is_clicked(event):
                auto = True if auto is False else False
                button_draft.color = 'Lime' if button_draft.color == 'SteelBlue' else 'SteelBlue'
                break
            elif button_go.is_clicked(event):
                go = True
                todo = True
                button_go.color = 'Lime'
                break
            elif button_new.is_clicked(event):
                input_sudo = sudokum.generate(mask_rate=0.5)
                button_new.color = 'Lime'
                for i in range(1, 10):
                    for j in range(1, 10):
                        if input_sudo[i - 1][j - 1] == 0:
                            board[str(i) + str(j)] = [0]
                        else:
                            board[str(i) + str(j)] = [input_sudo[i - 1][j - 1]]
                for i in range(1, 10):
                    for j in range(1, 10):
                        cell_matrix[str(i) + str(j)] = Cell()
                auto = False
                todo = True
                running = False

                count = 0
                msg = ''
                data = [0, 0, 0, 0]
                msg_display = []
            else:
                pass
            for idx, cell in cell_matrix.items():
                if cell.x is None:
                    continue
                if cell.is_clicked(event):
                    if idx == cur_cell:
                        cell.lock = 0
                        cur_cell = 0
                        for fi in rel_cells:
                            cell_matrix[fi].lock = 0
                        for fi in rel_value_cells:
                            cell_matrix[fi].lock = 0
                        break
                    cell.lock = 1
                    cur_cell = idx

                    for fi in rel_cells:
                        cell_matrix[fi].lock = 0
                    for fi in rel_value_cells:
                        cell_matrix[fi].lock = 0
                    rel_cells = []
                    rel_value_cells = []

                    if len(cell.text) == 1 and cell.text[0]=='':
                        continue


                    for nn in range(1, 10):
                        rel_cells.append(str(nn) + str(idx)[1])
                        rel_cells.append(str(idx)[0] + str(nn))

                    cur_v = board[idx][0]
                    for iii in range(1, 10):
                        for jjj in range(1, 10):
                            v = board[str(iii) + str(jjj)]
                            if len(v) == 1 and v[0] == cur_v:
                                rel_value_cells.append(str(iii) + str(jjj))
                    for rel_idx in rel_cells:
                        cell_matrix[rel_idx].lock = 1
                    for rel_idx in rel_value_cells:
                        cell_matrix[rel_idx].lock = 2

            for n, bt in button_num.items():
                if cur_cell != 0 and bt.is_clicked(event):
                    board[cur_cell] = [int(n)]

            if running:
                button_num_cnt = {i:0 for i in range(1,10)}
                for ii in range(1,10):
                    for jj in range(1,10):
                        v = board[str(ii)+str(jj)]
                        if len(v)==1:
                            vv = v[0]
                            button_num_cnt[vv]+=1


                
    if todo and (auto or go):
        msg, data = update(board)
        count += 1
        if msg not in msg_display:
            msg_display.append(msg)
            if len(msg_display) > 40:
                msg_display.pop(0)
        if msg == 'Done':
            todo = False

    screen.fill(color['bg'])
    button_go.draw(screen)
    button_draft.draw(screen)
    button_new.draw(screen)

    for n, bt in button_num.items():
        if button_num_cnt[n]>0:
            bt.draw(screen)

    # # 画格子
    g_size = size['grid']
    g_margin = size['grid_margin']
    for i in range(1, 11):
        line_width = size['grid_line'] if i in [1, 4, 7, 10] else size['grid_line_light']
        pygame.draw.line(screen, color['line'], (i * g_size - g_margin, g_size - g_margin), (i * g_size - g_margin, g_size * 10 - g_margin), line_width)
        pygame.draw.line(screen, color['line'], (g_size - g_margin, i * g_size - g_margin), (g_size * 10 - g_margin, i * g_size - g_margin), line_width)

    cell_margin = size['cell_margin']
    for i in range(1, 10):
        for j in range(1, 10):
            if str(i) + str(j) not in board:
                continue
            v = board[str(i) + str(j)]
            cell = cell_matrix[str(i) + str(j)]

            if len(v) == 1:
                if i == data[0] and j == data[1]:
                    cell.cell_type = 2
                else:
                    cell.cell_type = 0
                cell.x = j * g_size + cell_margin
                cell.y = i * g_size + cell_margin
                if str(v[0]) == '0':
                    cell.text = ['']
                else:
                    cell.text = [str(v[0])]
                cell.draw(screen)
            else:
                if i == data[2] and j == data[3]:
                    cell.cell_type = 3
                else:
                    cell.cell_type = 1
                t = [str(xi) if xi in v else '    ' for xi in range(1, 10)]
                display_v = [
                    '  ' + t[0] + '    ' + t[1] + '    ' + t[2],
                    '  ' + t[3] + '    ' + t[4] + '    ' + t[5],
                    '  ' + t[6] + '    ' + t[7] + '    ' + t[8]
                ]
                cell = cell_matrix[str(i) + str(j)]
                cell.x = j * g_size + cell_margin
                cell.y = i * g_size + cell_margin
                cell.text = display_v
                cell.draw(screen)





    if finish(board):
        for idx, cell in board.items():
            cell_matrix[idx].lock = 3


    info_list = ['step:  ' + str(count), ''] + msg_display
    pi = pos['msg'][1]
    for info in info_list:
        font = pygame.font.SysFont("Arial", size['cell_radius_draft'])
        txt = font.render(info, True, color['msg'])
        screen.blit(txt, (pos['msg'][0], pi))
        pi += 15
    pygame.display.flip()
    dt = clock.tick(30)
    button_go.color = 'SteelBlue'
    button_new.color = 'SteelBlue'
